"""Regress optical observation, immutable receipt validation and rendered credits.

The optical calculation and profile checks are the actual shipped functions.
The synthetic profile/data exercise bookkeeping and algebra only, not physical
fNIRS validation. All execution evidence is generated in temporary directories.
"""
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import textwrap

HERE = Path(__file__).resolve().parent
APP = HERE.parents[1]
sys.path.insert(0, str(HERE))
import credits

MODULE = "optical_signal_review_v1_0"
METHOD = "optical_verified_relative_hemoglobin"
PRIMARY_URL = "https://doi.org/10.1088/0031-9155/33/12/008"
MNE_URL = "https://mne.tools/stable/auto_tutorials/preprocessing/70_fnirs_processing.html"


def load(name, relative):
    spec = importlib.util.spec_from_file_location(name, APP / relative)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def test_all_current_method_references_satisfy_receipt_contract():
    registry = credits.read_registry()
    for method_id, method in registry["methods"].items():
        assert isinstance(method["references"], list), method_id
        for reference in method["references"]:
            assert all(isinstance(reference.get(key), str) and reference[key].strip()
                       for key in ("id", "citation", "url")), (method_id, reference)
        source = APP / method["source"]
        assert hashlib.sha256(source.read_bytes()).hexdigest() == method["source_sha256"], method_id


def test_observed_optical_conversion_survives_receipt_aggregation_and_html(tmp_path):
    registry = credits.read_registry()
    source = APP / registry["methods"][METHOD]["source"]
    worker = tmp_path / "synthetic_optical_worker.py"
    output = tmp_path / "output"
    worker.write_text(textwrap.dedent(f"""
        import importlib.util
        import json
        from pathlib import Path
        import numpy as np
        spec = importlib.util.spec_from_file_location('observed_optical', {str(source)!r})
        optical = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(optical)
        root = Path(__file__).parent
        evidence = root / 'synthetic_profile_evidence.txt'
        evidence.write_text('Synthetic algebra fixture only; no measured instrument or participant data.')
        profile = dict(schema=optical.PROFILE_SCHEMA, status='VERIFIED',
            run_uuid='synthetic-optical-credit-1141', xdf_sha256='synthetic-xdf-hash',
            stream_source_id='synthetic-source', constant_gain_verified=True,
            baseline_seconds=1,
            evidence=[dict(relative_path=evidence.name, sha256=optical.core.sha256_file(evidence))],
            mapping=[dict(name='synthetic-pair', channel_labels=['a','b'],
                wavelengths_nm=[760,850], source_position_m=[0,0,0],
                detector_position_m=[.03,0,0], distance_m=.03,
                partial_pathlength_factors=[6,6],
                extinction_natural_log_m_inverse_per_molar=[[100,300],[250,150]])])
        profile['canonical_sha256'] = optical.eeg.sha256_json(profile)
        profile_path = root / 'synthetic_profile.json'
        profile_path.write_text(json.dumps(profile), encoding='utf-8')
        verified = optical.verify_profile(profile_path, 'synthetic-xdf-hash',
            'synthetic-optical-credit-1141', 'synthetic-source', ['a','b'])
        time = np.arange(0,3,.01)
        target = np.zeros((len(time),2))
        target[time >= 1] = [2e-6,-.5e-6]
        mapping = verified['mapping'][0]
        matrix = np.diag(np.asarray(mapping['partial_pathlength_factors']) * mapping['distance_m']) @ np.asarray(mapping['extinction_natural_log_m_inverse_per_molar'])
        intensity = 10000 * np.exp(-(matrix @ target.T).T)
        recovered, mask, names = optical.hemoglobin(intensity, time, ['a','b'],
            np.ones(intensity.shape, bool), verified, 0)
        np.testing.assert_allclose(recovered[:,0], target * 1e6, atol=1e-10)
        assert mask.all() and names == ['synthetic-pair']
        output = Path({str(output)!r})
        output.mkdir()
        np.savez(output / 'synthetic_relative_hemoglobin.npz',
            concentration_um=recovered, valid_mask=mask)
    """), encoding="utf-8")
    receipt_id = "synthetic-optical-credits-1141"
    sidecar = tmp_path / "observed_credits.json"
    protected = [source, HERE / "run_with_credits.py", HERE / "credits.py",
                 APP / "config/attribution_registry_v1.json"]
    before = {str(path): hashlib.sha256(path.read_bytes()).hexdigest() for path in protected}
    completed = subprocess.run([sys.executable, str(HERE / "run_with_credits.py"),
        "--module", MODULE, "--receipt", receipt_id, "--credits", str(sidecar),
        "--", str(worker)], capture_output=True, text=True, timeout=90,
        env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
    assert completed.returncode == 0, completed.stdout + completed.stderr
    observed = json.loads(sidecar.read_text(encoding="utf-8"))
    assert observed["source_mismatches"] == []
    expected_coverage = ("WORKER_PROCESS_ONLY_DESCENDANTS_UNOBSERVED"
                         if observed["descendant_process_count"] else "WORKER_PROCESS_ONLY")
    assert observed["coverage"] == expected_coverage
    assert observed["exit_code"] == 0
    assert observed["registry_sha256"] == credits.digest(registry)
    assert observed["content_sha256"] == credits.digest({k:v for k,v in observed.items() if k != "content_sha256"})
    assert [row["method_id"] for row in observed["observed_methods"]] == [METHOD]
    assert observed["observed_methods"][0]["observation"] == "FUNCTION_ENTERED"
    assert any(row["name"].lower() == "numpy" for row in observed["observed_distributions"])
    assert {str(path): hashlib.sha256(path.read_bytes()).hexdigest() for path in protected} == before

    orchestrator = load("optical_credit_orchestrator_1141",
        "tools/Analysis_Orchestrator_v0_1/praycg_analysis_orchestrator_v0_1.py")
    receipt = orchestrator.update_execution_receipt({
        "schema": orchestrator.EXECUTION_RECEIPT_SCHEMA,
        "receipt_id": receipt_id, "module_id": MODULE, "attribution": observed},
        status="COMPLETE", output_path=output)
    assert orchestrator.validate_execution_receipt_artifacts(receipt)["status"] == "PASS"
    original = copy.deepcopy(receipt)
    report = credits.aggregate({"modules": [{"module_id": MODULE}]}, [receipt])
    assert report["attempts"][0]["credits_state"] == expected_coverage
    assert [row["method_id"] for row in report["attempts"][0]["methods"]] == [METHOD]
    assert {row["url"] for row in report["bibliography"]} >= {PRIMARY_URL, MNE_URL}
    assert any(row["name"].lower() == "numpy" for row in report["software"])
    rendered = credits.report_html(report)
    assert "Delpy" in rendered and "1988" in rendered and PRIMARY_URL in rendered
    assert "MNE-Python" in rendered and MNE_URL in rendered and "numpy" in rendered.lower()
    assert receipt == original, "Rendering must not rewrite immutable receipt evidence."


def test_malformed_historical_optical_credit_is_not_silently_repaired():
    method = copy.deepcopy(credits.read_registry()["methods"][METHOD])
    method["references"] = [{"url": MNE_URL}]
    observed = {"schema": credits.SCHEMA, "receipt_id": "historical",
        "module_id": MODULE, "coverage": "WORKER_PROCESS_ONLY",
        "observed_methods": [method], "observed_distributions": [{"name": "numpy", "version": "historical"}]}
    observed["content_sha256"] = credits.digest(observed)
    receipt = {"receipt_id": "historical", "module_id": MODULE,
               "status": "COMPLETE", "attribution": observed}
    original = copy.deepcopy(receipt)
    report = credits.aggregate({"modules": [{"module_id": MODULE}]}, [receipt])
    assert report["attempts"][0]["credits_state"] == "NOT_RECORDED_OR_INVALID"
    assert report["bibliography"] == report["software"] == []
    assert receipt == original
