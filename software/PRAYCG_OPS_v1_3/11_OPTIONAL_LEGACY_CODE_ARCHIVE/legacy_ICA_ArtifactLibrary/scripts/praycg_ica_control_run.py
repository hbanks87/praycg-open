#!/usr/bin/env python3
"""
PR-AYC-G ICA Artifact Control Run
=================================

Run this inside PsychoPy Standalone/Coder or a Python environment with PsychoPy installed.
It presents a structured artifact library session and sends LSL markers so the resulting XDF can
be used to train/inspect ICA artifact components.

Recommended stream stack before clicking Start in this script:
  - OpenBCI EEG stream, e.g. obci_eeg1
  - Optional: PolarHRV / PolarECG
  - Optional: VernierRespirationBelt
  - ICAArtifactMarkers created by this script
  - LabRecorder actively recording all streams

Output:
  - XDF from LabRecorder
  - local CSV/JSON marker log from this script

The session intentionally records artifacts. It is not a PR-AYC-G evidence run.
"""

from __future__ import annotations

import csv
import json
import sys
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Optional

try:
    from psychopy import visual, core, event, gui
except Exception as exc:  # pragma: no cover
    raise RuntimeError("This script needs PsychoPy. Run it from PsychoPy Standalone/Coder or install psychopy.") from exc

try:
    from pylsl import StreamInfo, StreamOutlet, resolve_byprop, local_clock
except Exception as exc:  # pragma: no cover
    raise RuntimeError("pylsl is required. In PsychoPy Shell: import sys, subprocess; subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pylsl'])") from exc


@dataclass
class RunConfig:
    participant_id: str = "Hoyt"
    session_id: str = "ICA_ARTIFACT_LIBRARY"
    screen_index: int = 0
    fullscr: bool = True
    window_width: int = 1920
    window_height: int = 1080
    fixation_height: int = 60
    rest_before_each_sec: float = 4.0
    prep_countdown_sec: float = 2.0
    event_plan_csv: str = "../config/artifact_event_plan.csv"
    output_dir: str = "../outputs/ica_artifact_control_logs"
    marker_stream_name: str = "ICAArtifactMarkers"
    marker_source_id: str = "praycg_ica_artifact_marker_01"
    required_lsl_streams: str = "obci_eeg1"
    optional_lsl_streams: str = "PolarHRV,VernierRespirationBelt,PolarECG"


class AbortSession(Exception):
    pass


class LocalLogger:
    def __init__(self, outdir: Path, config: RunConfig):
        outdir.mkdir(parents=True, exist_ok=True)
        stamp = time.strftime("%Y%m%d_%H%M%S")
        base = f"{config.session_id}_{config.participant_id}_{stamp}"
        self.csv_path = outdir / f"{base}_marker_log.csv"
        self.json_path = outdir / f"{base}_marker_log.json"
        self.config_path = outdir / f"{base}_config.json"
        self.rows: List[Dict] = []
        self.f = open(self.csv_path, "w", newline="", encoding="utf-8")
        self.writer = csv.DictWriter(
            self.f,
            fieldnames=["marker", "lsl_time", "unix_time", "psychopy_time", "artifact_label", "rep", "phase", "note"],
        )
        self.writer.writeheader()
        with open(self.config_path, "w", encoding="utf-8") as cf:
            json.dump(asdict(config), cf, indent=2)

    def write(self, marker: str, artifact_label: str = "", rep: Optional[int] = None, phase: str = "", note: str = ""):
        row = dict(
            marker=marker,
            lsl_time=local_clock(),
            unix_time=time.time(),
            psychopy_time=core.getTime(),
            artifact_label=artifact_label,
            rep="" if rep is None else rep,
            phase=phase,
            note=note,
        )
        self.rows.append(row)
        self.writer.writerow(row)
        self.f.flush()
        print(f"[MARKER] {marker}")

    def close(self):
        try:
            with open(self.json_path, "w", encoding="utf-8") as jf:
                json.dump(self.rows, jf, indent=2)
        finally:
            try:
                self.f.close()
            except Exception:
                pass


def push_marker(outlet: StreamOutlet, logger: LocalLogger, marker: str, artifact_label: str = "", rep: Optional[int] = None, phase: str = "", note: str = ""):
    outlet.push_sample([marker], timestamp=local_clock())
    logger.write(marker, artifact_label=artifact_label, rep=rep, phase=phase, note=note)


def schedule_marker(win: visual.Window, outlet: StreamOutlet, logger: LocalLogger, marker: str, artifact_label: str = "", rep: Optional[int] = None, phase: str = "", note: str = ""):
    win.callOnFlip(push_marker, outlet, logger, marker, artifact_label, rep, phase, note)


def check_escape(outlet: StreamOutlet, logger: LocalLogger, win: Optional[visual.Window] = None):
    keys = event.getKeys(keyList=["escape"])
    if keys:
        push_marker(outlet, logger, "ICA_ARTIFACT_LIBRARY_EMERGENCY_KILL", phase="ABORT")
        if win:
            win.close()
        raise AbortSession("Escape pressed")


def resolve_stream_status(required: List[str], optional: List[str]) -> Dict[str, bool]:
    status = {}
    for name in required + optional:
        if not name:
            continue
        try:
            status[name] = bool(resolve_byprop("name", name, timeout=1.25))
        except Exception:
            status[name] = False
    return status


def load_event_plan(path: Path) -> List[Dict]:
    if not path.exists():
        raise FileNotFoundError(f"Artifact event plan not found: {path}")
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(
                dict(
                    artifact_label=str(r["artifact_label"]).strip(),
                    category=str(r.get("category", "")).strip(),
                    prompt=str(r["prompt"]).strip(),
                    repetitions=int(float(r.get("repetitions", 1))),
                    action_seconds=float(r.get("action_seconds", 2)),
                    recovery_seconds=float(r.get("recovery_seconds", 4)),
                    notes=str(r.get("notes", "")).strip(),
                )
            )
    return rows


def show_text(win: visual.Window, text: str, height: int = 34, wrap: int = 1500):
    stim = visual.TextStim(win, text=text, color="white", height=height, wrapWidth=wrap, alignText="center")
    stim.draw()
    win.flip()


def draw_fixation(win: visual.Window, height: int = 60):
    stim = visual.TextStim(win, text="+", color="white", height=height)
    stim.draw()


def wait_for_space_or_right_click(win: visual.Window):
    mouse = event.Mouse(win=win)
    mouse.clickReset()
    event.clearEvents()
    while True:
        if "space" in event.getKeys(keyList=["space"]):
            return
        if mouse.getPressed()[2]:
            return
        core.wait(0.05)


def timed_fixation(win: visual.Window, seconds: float, outlet: StreamOutlet, logger: LocalLogger, config: RunConfig):
    clock = core.Clock()
    while clock.getTime() < seconds:
        check_escape(outlet, logger, win)
        draw_fixation(win, config.fixation_height)
        win.flip()


def run_action_block(
    win: visual.Window,
    outlet: StreamOutlet,
    logger: LocalLogger,
    config: RunConfig,
    artifact_label: str,
    rep: int,
    prompt: str,
    action_seconds: float,
    recovery_seconds: float,
):
    # Rest before event.
    schedule_marker(win, outlet, logger, f"ARTIFACT_{artifact_label}_REP_{rep}_PREP_START", artifact_label, rep, "PREP_START")
    draw_fixation(win, config.fixation_height)
    win.flip()
    timed_fixation(win, config.rest_before_each_sec, outlet, logger, config)

    # Prompt/prep countdown.
    prep_msg = (
        f"{artifact_label}  |  repetition {rep}\n\n"
        f"Prepare:\n{prompt}\n\n"
        "When the ACTION screen appears, perform the movement exactly once/as instructed.\n"
        "Then immediately relax.\n\n"
        "Press SPACE or RIGHT-CLICK when ready. ESC aborts."
    )
    show_text(win, prep_msg, height=30)
    wait_for_space_or_right_click(win)
    for n in range(int(config.prep_countdown_sec), 0, -1):
        show_text(win, f"Prepare\n\n{n}", height=70)
        core.wait(1.0)
        check_escape(outlet, logger, win)

    # Action.
    action_stim = visual.TextStim(
        win,
        text=f"ACTION\n\n{prompt}",
        color="white",
        height=40,
        wrapWidth=1500,
        alignText="center",
    )
    action_stim.draw()
    schedule_marker(win, outlet, logger, f"ARTIFACT_{artifact_label}_REP_{rep}_ACTION_START", artifact_label, rep, "ACTION_START")
    win.flip()
    clock = core.Clock()
    while clock.getTime() < action_seconds:
        check_escape(outlet, logger, win)
        action_stim.draw()
        win.flip()

    # Recovery.
    rec_stim = visual.TextStim(win, text="RELAX\n\nFace, jaw, neck, shoulders soft. Eyes on +.", color="white", height=38, wrapWidth=1500)
    rec_stim.draw()
    schedule_marker(win, outlet, logger, f"ARTIFACT_{artifact_label}_REP_{rep}_ACTION_END", artifact_label, rep, "ACTION_END")
    win.flip()
    rec_clock = core.Clock()
    while rec_clock.getTime() < recovery_seconds:
        check_escape(outlet, logger, win)
        draw_fixation(win, config.fixation_height)
        win.flip()
    draw_fixation(win, config.fixation_height)
    schedule_marker(win, outlet, logger, f"ARTIFACT_{artifact_label}_REP_{rep}_RECOVERY_END", artifact_label, rep, "RECOVERY_END")
    win.flip()


def show_config_dialog(config: RunConfig, stream_status: Dict[str, bool]) -> bool:
    dlg = gui.Dlg(title="PR-AYC-G ICA Artifact Library Control Run")
    req = [x.strip() for x in config.required_lsl_streams.split(",") if x.strip()]
    opt = [x.strip() for x in config.optional_lsl_streams.split(",") if x.strip()]
    dlg.addText("Required LSL streams:")
    dlg.addText("\n".join([f"{'OK' if stream_status.get(x) else 'MISSING'}: {x}" for x in req]) or "None")
    dlg.addText("\nOptional LSL streams:")
    dlg.addText("\n".join([f"{'OK' if stream_status.get(x) else 'not found'}: {x}" for x in opt]) or "None")
    dlg.addText("\nStart LabRecorder BEFORE beginning this run.")
    dlg.addField("Participant ID", config.participant_id)
    dlg.addField("Session ID", config.session_id)
    dlg.addField("Screen index", config.screen_index)
    dlg.addField("Fullscreen", config.fullscr)
    dlg.show()
    if not dlg.OK:
        return False
    config.participant_id = str(dlg.data[0]).strip() or config.participant_id
    config.session_id = str(dlg.data[1]).strip() or config.session_id
    config.screen_index = int(dlg.data[2])
    config.fullscr = bool(dlg.data[3])
    return True


def main():
    here = Path(__file__).resolve().parent
    config = RunConfig()
    event_plan_path = (here / config.event_plan_csv).resolve()
    output_dir = (here / config.output_dir).resolve()
    plan = load_event_plan(event_plan_path)

    info = StreamInfo(config.marker_stream_name, "Markers", 1, 0, "string", config.marker_source_id)
    outlet = StreamOutlet(info)
    core.wait(0.5)

    required = [x.strip() for x in config.required_lsl_streams.split(",") if x.strip()]
    optional = [x.strip() for x in config.optional_lsl_streams.split(",") if x.strip()]
    status = resolve_stream_status(required, optional)
    if not show_config_dialog(config, status):
        core.quit()

    logger = LocalLogger(output_dir, config)
    win: Optional[visual.Window] = None
    try:
        push_marker(outlet, logger, "ICA_ARTIFACT_MARKER_STREAM_ONLINE", phase="SETUP")
        win = visual.Window(
            size=(config.window_width, config.window_height),
            screen=config.screen_index,
            fullscr=config.fullscr,
            color=[-1, -1, -1],
            units="pix",
            allowGUI=False,
            waitBlanking=True,
        )
        intro = (
            "ICA Artifact Library Control Run\n\n"
            "This is not a PR-AYC-G evidence run.\n"
            "It intentionally records blinks, jaw, neck, shoulder, swallow, breathing, and clean stillness.\n\n"
            "Keep movements gentle. Do not force pain, breath holds, or excessive clenching.\n"
            "After each action, immediately relax.\n\n"
            "Confirm LabRecorder is already recording.\n\n"
            "Press SPACE or RIGHT-CLICK to begin. ESC aborts."
        )
        show_text(win, intro, height=32)
        wait_for_space_or_right_click(win)

        schedule_marker(win, outlet, logger, "ICA_ARTIFACT_LIBRARY_START", phase="PROTOCOL_START")
        win.flip()
        core.wait(0.5)

        for item in plan:
            label = item["artifact_label"]
            block_start = f"ARTIFACT_{label}_BLOCK_START"
            schedule_marker(win, outlet, logger, block_start, artifact_label=label, phase="BLOCK_START", note=item.get("notes", ""))
            show_text(win, f"Next block:\n\n{label}\n\n{item['notes']}\n\nPress SPACE or RIGHT-CLICK.", height=34)
            wait_for_space_or_right_click(win)
            for rep in range(1, item["repetitions"] + 1):
                run_action_block(
                    win,
                    outlet,
                    logger,
                    config,
                    artifact_label=label,
                    rep=rep,
                    prompt=item["prompt"],
                    action_seconds=item["action_seconds"],
                    recovery_seconds=item["recovery_seconds"],
                )
            schedule_marker(win, outlet, logger, f"ARTIFACT_{label}_BLOCK_END", artifact_label=label, phase="BLOCK_END")
            win.flip()
            core.wait(0.25)

        schedule_marker(win, outlet, logger, "ICA_ARTIFACT_LIBRARY_END", phase="PROTOCOL_END")
        win.flip()
        show_text(win, "ICA artifact library run complete.\n\nStop LabRecorder after this screen.\n\nThank you.", height=40)
        core.wait(3.0)

    except AbortSession as exc:
        print(f"Aborted: {exc}")
    except Exception as exc:
        push_marker(outlet, logger, "ICA_ARTIFACT_LIBRARY_ERROR", phase="ERROR", note=repr(exc))
        raise
    finally:
        if win is not None:
            try:
                win.close()
            except Exception:
                pass
        logger.close()
        core.quit()


if __name__ == "__main__":
    main()
