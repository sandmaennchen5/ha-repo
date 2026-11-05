import json
import os
from pathlib import Path
import unittest
from unittest.mock import mock_open, patch

import yaml

ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = yaml.safe_load((ROOT / ".github/workflows/update-apps.yaml").read_text(encoding="utf-8"))
PLAN = next(step["run"] for step in WORKFLOW["jobs"]["update"]["steps"]
            if step.get("id") == "build_plan")
CODE = PLAN.split("python - <<'PY'\n", 1)[1].split("\nPY", 1)[0]


class LocalBuildPlanTests(unittest.TestCase):
    def classify(self, apps):
        output = mock_open()
        configs = {"local": {}, "published": {"image": "ghcr.io/example/test"}}

        def read_config(path, **kwargs):
            return json.dumps(configs[path.parent.name])

        with patch.dict(os.environ, BUILT_APPS=json.dumps(apps), GITHUB_OUTPUT="output"), \
             patch.object(Path, "read_text", read_config), \
             patch("builtins.open", output):
            exec(CODE, {})
        written = "".join(call.args[0] for call in output().write.call_args_list)
        return json.loads(written.strip().split("=", 1)[1])

    def test_local_builds_require_no_size_artifacts(self):
        self.assertEqual(self.classify(["local"]), [])

    def test_published_and_mixed_builds_still_collect_sizes(self):
        self.assertEqual(self.classify(["published"]), ["published"])
        self.assertEqual(self.classify(["local", "published"]), ["published"])

    def test_empty_build_plan(self):
        self.assertEqual(self.classify([]), [])


if __name__ == "__main__":
    unittest.main()
