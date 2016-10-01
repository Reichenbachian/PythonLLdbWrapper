# PythonLLdbWrapper
There is a python library for lldb. But there is no documentation and it is impossible to understand or read. So I've taken some of the more common methods and written wrappers around them. Please add any functions you want, so we can have a *working* lldb python implementation.

This only works with default python. That's not an implementation error on my part, but rather a necessity of lldb python bindings. If python crashes when you import lldb, try removing the python/pyenv shims from your path variable(Or any other impedence to lldb reaching system python easily).