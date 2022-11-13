import subprocess


def test_script():
	result = subprocess.run(
		[
			"coverage",
			"run",
			"-m",
			"factotum",
			"tests/assets/func_other_name.py",
			"run",
			"--name",
			"Camila",
		],
		stdout = subprocess.PIPE,
		stderr = subprocess.PIPE,
		encoding = "utf-8",
	)
	assert "Hello Camila" in result.stdout
