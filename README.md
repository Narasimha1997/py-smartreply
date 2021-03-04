## Py-Smartreply
Python bindings for Google's Smart Reply Tensorflow Lite model. 
This is the much cleaner and easily deployable version of [Smartreply](https://github.com/Narasimha1997/smartreply) which I built earlier.

### Features:
1. Python package which can be used end-to-end without any dependencies.
2. Uses CMake build-system, to build C++ codebase (Earlier Repository used bazel)
3. Custom Tensorflow Lite op-resolver, which binds C++ operators to the Directed-Acyclic-Graph at Compile-Time.
4. A Web-server written in Flask, which serves the model for inference over a REST API.
5. Kubernetes deployment configuration.

### Why another repository?
The earlier version used `bazel` build-system, which led to many build issues. Bazel has poor interoperability with Python build-system. It was literally impossible to build and deploy a python package on the fly, in an automated, hassle-free manner. The newer version of Smartreply uses `CMake`, which makes it easy to integrate with python build-system, now the build is automated and does not require any intervention (or manual steps in between), this allows us to write CI/CD pipelines with GitHub actions and automate the entire code-test-package-deploy cycle. The earlier version was also dependant on a function called `RegisterSelectedOps`, this was a dynamically generating function at compile-time (as a header file) and Google somehow automated it with Bazel, which was not possible with CMake, thus the newer version removed its dependency and impelementes it's own op-resolver function, which hardcodes the operators rather than generating a function and linking it at compile-time dynamically.

### How to build:
To build this package, you may require `CMake` and `skbuild` which are easily installable. Once you have installed these packages, run:
```
python3 setup.py bdist_wheel
```

### Using package from PyPI:
You can install this package via pip, as follows:
```
pip install py_smartreply

#or 

pip install py-smartreply
```

### Usage
The example below shows the usage:

```python3
from smartreply import SmartReplyRuntime

#create SmartReplyRuntime() object, you can specify your own model path as an argument, or default provided 
#model will be used, ex : SmartReplyRuntime('mymodel.tflite')
rt = SmartReplyRuntime()

#Prediction on a single string
single = rt.predict("hi")
print(single)

#Prediction on multiple strings, runs in a loop
multi = rt.predictMultiple(["hello", "i am happy", "great"])
print(multi)

#Prediction on multiple strings, exploits batching capability of tflite
multiBatch = rt.predictMultiple(["hello", "i am happy", "see me tomorrow"], batch = True)
print(multiBatch)
```

### Using the REST API
Start the server normally, as follows:
```
python3 web-server/app.py
```

This will start the server on PORT `8000`, then you can use curl to test:
#### Singe Input Request:
```
curl -d '{"input" : "Hello"}' -H "Content-Type:application/json" http://localhost:8000/api/inference
```

Output:
```
{"result":{"Hi, how are you doing?":1.0899782180786133,"How are you sir?":1.4489225149154663,"I do not understand":1.1177111864089966,"No pictures":0.4019201695919037,"Sending now":0.4459223747253418,"So how did it go?":1.0521267652511597},"success":true}
```

#### Multiple Inputs Request:
```
curl -d '{"input" : ["Hello", "hi", "I am happy"]}' -H "Content-Type:application/json" http://localhost:8000/api/inference
```

### Using the Dockerfile
The `Dockerfile` can be found at `web-server/Dockerfile`. You can build and run as follows:

1. Build:
```
cd web-server
docker build . -t smartreply:latest
```
2. Run:
docker run --rm -ti -p 8000:8000 smartreply:latest

### Deploy on K8s
The deplpyment file is located at `web-server/kubernetes/deploy.yaml`.
If you have a K8s cluster and `kubectl` installed, you can try:
```
kubectl create -f web-server/kubernetes/deploy.yaml
```

### Running tests:
The project uses `pytest` for testing the functionalities, tests can be found at `tests/test_smartreply.py`.
You can run the test suite as follows:

```
pytest tests/
```

### Contributing:
Contributions of any sort are always welcome. You can raise issues, suggest features or make PRs directly, if you find something can be better or need to add any feature that can help others.
