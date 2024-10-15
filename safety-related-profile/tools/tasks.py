from invoke import task

@task
def depend(c, docs=False):
     c.run("python -m onnx_depend --model_path LeNet5.onnx")
