twosheds
========

Twosheds is a shell written in Python. It is intended to be highly extensible.

# Install

```
pip install twosheds
```

You may need to `sudo` if you intend to install system wide.

# Make twosheds your default shell

To make twosheds your default shell you need to complete two steps:

First note the location of twosheds via `echo $(which twosheds)`

1.  Add twosheds to `/etc/shells`.

    To do this you'll need to edit the file with root privileges and append to it the location of twosheds. 

2.  Run `chsh -s $(which twosheds)`
