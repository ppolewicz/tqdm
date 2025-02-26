|Logo|

tqdm
====

|PyPi Status| |PyPi Downloads|
|Build Status| |Coverage Status| |Branch Coverage Status|

``tqdm`` (read taqadum, تقدّم) means "progress" in arabic.

Instantly make your loops show a smart progress meter - just wrap any
iterable with "tqdm(iterable)", and you're done!

.. code:: python

    from tqdm import tqdm
    for i in tqdm(range(9)):
        ...

Here's what the output looks like:

76%\|████████████████████\             \| 7641/10000 [00:34<00:10,
222.22 it/s]

``trange(N)`` can be also used as a convenient shortcut for
``tqdm(xrange(N))``.

|Screenshot|

Overhead is low -- about 60ns per iteration (80ns with ``gui=True``).
By comparison, the well established
`ProgressBar <https://github.com/niltonvolpato/python-progressbar>`__ has
an 800ns/iter overhead.

In addition to its low overhead, ``tqdm`` uses smart algorithms to predict
the remaining time and to skip unnecessary iteration displays, which allows
for a negligible overhead in most cases.

``tqdm`` works on any platform (Linux/Windows/Mac), in any console or in a
GUI, and is also friendly with IPython/Jupyter notebooks.

``tqdm`` does not require any library (not even curses!) to run, just a
vanilla Python interpreter will do.

------------------------------------------

.. contents:: Table of contents
   :backlinks: top
   :local:


Installation
------------

Latest pypi stable release
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: sh

    pip install tqdm

Latest development release on github
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pull and install in the current directory:

.. code:: sh

    pip install -e git+https://github.com/tqdm/tqdm.git@master#egg=tqdm


Usage
-----

``tqdm`` is very versatile and can be used in a number of ways.
The two main ones are given below.

Iterable-based
~~~~~~~~~~~~~~

Wrap ``tqdm()`` around any iterable:

.. code:: python

    for char in tqdm(["a", "b", "c", "d"]):
        print char

``trange(i)`` is a special optimised instance of ``tqdm(range(i))``:

.. code:: python

    for i in trange(100):
        pass

Instantiation outside of the loop allows for manual control over ``tqdm()``:

.. code:: python

    pbar = tqdm(["a", "b", "c", "d"])
    for char in pbar:
        pbar.set_description("Processing %s" % char)

Stream-based
~~~~~~~~~~~~~~

Wrap ``tqdm()`` around a file-like object:

.. code:: python

    for line in tqdm(stream=open('big-file.dat', 'rb')):
        print char

``trange(i)`` is a special optimised instance of ``tqdm(range(i))``:

.. code:: python

    for i in trange(100):
        pass
Manual
~~~~~~

Manual control on ``tqdm()`` updates by using a ``with`` statement:

.. code:: python

    with tqdm(total=100) as pbar:
        for i in range(10):
            pbar.update(10)

If the optional variable ``total`` (or an iterable with ``len()``) is
provided, predictive stats are displayed.

``with`` is also optional (you can just assign ``tqdm()`` to a variable,
but in this case don't forget to ``close()`` at the end:

.. code:: python

    pbar = tqdm(total=100):
    for i in range(10):
        pbar.update(10)
    pbar.close()


Documentation
-------------

.. code:: python

    class tqdm(object):
      """
      Decorate an iterable object, returning an iterator which acts exactly
      like the original iterable, but prints a dynamically updating
      progressbar every time a value is requested.
      """

      def __init__(self, iterable=None, desc=None, total=None, leave=False,
                   file=sys.stderr, ncols=None, mininterval=0.1,
                   maxinterval=10.0, miniters=None, ascii=None, disable=False,
                   unit='it', unit_scale=False, dynamic_ncols=False,
                   smoothing=0.3, nested=False, stream=None):

Parameters
~~~~~~~~~~

* iterable  : iterable, optional  
    Iterable to decorate with a progressbar.
    Leave blank [default: None] to manually manage the updates.
* desc  : str, optional  
    Prefix for the progressbar [default: None].
* total  : int, optional  
    The number of expected iterations. If not given, len(iterable)
    is used if possible. As a last resort, only basic progress
    statistics are displayed (no ETA, no progressbar). If `gui` is
    True and this parameter needs subsequent updating, specify an
    initial arbitrary large positive integer, e.g. int(9e9).
* leave  : bool, optional  
    If [default: False], removes all traces of the progressbar
    upon termination of iteration.
* file  : `io.TextIOWrapper` or `io.StringIO`, optional  
    Specifies where to output the progress messages
    [default: sys.stderr]. Uses `file.write(str)` and `file.flush()`
    methods.
* ncols  : int, optional  
    The width of the entire output message. If specified,
    dynamically resizes the progressbar to stay within this bound.
    If [default: None], attempts to use environment width. The
    fallback is a meter width of 10 and no limit for the counter and
    statistics. If 0, will not print any meter (only stats).
* mininterval  : float, optional  
    Minimum progress update interval, in seconds [default: 0.1].
* maxinterval  : float, optional
    Maximum progress update interval, in seconds [default: 10.0].
* miniters  : int, optional  
    Minimum progress update interval, in iterations [default: None].
    If specified, will set `mininterval` to 0.
* ascii  : bool, optional  
    If [default: None] or false, use unicode (smooth blocks) to fill
    the meter. The fallback is to use ASCII characters `1-9 #`.
* disable : bool  
    Whether to disable the entire progressbar wrapper
    [default: False].
* unit  : str, optional  
    String that will be used to define the unit of each iteration
    [default: 'it'].
* unit_scale  : bool, optional  
    If set, the number of iterations will be reduced/scaled
    automatically and a metric prefix following the
    International System of Units standard will be added
    (kilo, mega, etc.) [default: False].
* dynamic_ncols  : bool, optional  
    If set, constantly alters `ncols` to the environment (allowing
    for window resizes) [default: False].
* smoothing  : float  
    Exponential moving average smoothing factor for speed estimates
    (ignored in GUI mode). Ranges from 0 (average speed) to 1
    (current/instantaneous speed) [default: 0.3].
* nested  : bool, optional  
    Whether this iterable is nested in another one also managed by
    `tqdm` [default: False]. Allows display of multiple, nested
    progress bars.
* stream  : `io.BufferedReader` or `io.BufferedWriter`, optional  
    File-like object to decorate with a progressbar.

Returns
~~~~~~~

* out  : decorated iterator.

.. code:: python

      def update(self, n=1):
          """
          Manually update the progress bar, useful for streams
          such as reading files.
          E.g.:
          >>> t = tqdm(total=filesize) # Initialise
          >>> for current_buffer in stream:
          ...    ...
          ...    t.update(len(current_buffer))
          >>> t.close()
          The last line is highly recommended, but possibly not necessary if
          `t.update()` will be called in such a way that `filesize` will be
          exactly reached and printed.

          Parameters
          ----------
          n  : int
              Increment to add to the internal counter of iterations
              [default: 1].
          """

      def close(self):
          """
          Cleanup and (if leave=False) close the progressbar.
          """

    def trange(*args, **kwargs):
        """
        A shortcut for tqdm(xrange(*args), **kwargs).
        On Python3+ range is used instead of xrange.
        """

    class tqdm_gui(tqdm):
        """
        Experimental GUI version of tqdm!
        """

    def tgrange(*args, **kwargs):
        """
        Experimental GUI version of trange!
        """


Examples and Advanced Usage
---------------------------

See the `examples <https://github.com/tqdm/tqdm/tree/master/examples>`__ folder or
import the module and run ``help()``.

Hooks and callbacks
~~~~~~~~~~~~~~~~~~~

``tqdm`` can easily support callbacks/hooks and manual updates.
Here's an example with ``urllib``:

**urllib.urlretrieve documentation**

    | [...]
    | If present, the hook function will be called once
    | on establishment of the network connection and once after each
      block read
    | thereafter. The hook will be passed three arguments; a count of
      blocks
    | transferred so far, a block size in bytes, and the total size of
      the file.
    | [...]

.. code:: python

    import urllib
    from tqdm import tqdm

    def my_hook(t):
      """
      Wraps tqdm instance. Don't forget to close() or __exit__()
      the tqdm instance once you're done with it (easiest using `with` syntax).

      Example
      -------

      >>> with tqdm(...) as t:
      ...     reporthook = my_hook(t)
      ...     urllib.urlretrieve(..., reporthook=reporthook)

      """
      last_b = [0]

      def inner(b=1, bsize=1, tsize=None):
        """
        b  : int, optional
            Number of blocks just transferred [default: 1].
        bsize  : int, optional
            Size of each block (in tqdm units) [default: 1].
        tsize  : int, optional
            Total size (in tqdm units). If [default: None] remains unchanged.
        """
        if tsize is not None:
            t.total = tsize
        t.update((b - last_b[0]) * bsize)
        last_b[0] = b
      return inner

    eg_link = 'http://www.doc.ic.ac.uk/~cod11/matryoshka.zip'
    with tqdm(unit='B', unit_scale=True, leave=True, miniters=1,
              desc=eg_link.split('/')[-1]) as t:  # all optional kwargs
        urllib.urlretrieve(eg_link, filename='/dev/null',
                           reporthook=my_hook(t), data=None)

It is recommend to use ``miniters=1`` whenever there is potentially
large differences in iteration speed (e.g. downloading a file over
a patchy connection).

Pandas Integration
~~~~~~~~~~~~~~~~~~

Due to popular demand we've added support for ``pandas`` -- here's an example
for ``DataFrameGroupBy.progress_apply``:

.. code:: python

    import pandas as pd
    import numpy as np
    from tqdm import tqdm, tqdm_pandas

    df = pd.DataFrame(np.random.randint(0, 100, (100000, 6)))

    # Create and register a new `tqdm` instance with `pandas`
    # (can use tqdm_gui, optional kwargs, etc.)
    tqdm_pandas(tqdm())

    # Now you can use `progress_apply` instead of `apply`
    df.groupby(0).progress_apply(lambda x: x**2)

In case you're interested in how this works (and how to modify it for your
own callbacks), see the `examples <https://github.com/tqdm/tqdm/tree/master/examples>`__
folder or import the module and run ``help()``.

Nested progress bars
~~~~~~~~~~~~~~~~~~~~

``tqdm`` supports nested progress bars, you just need to specify the
`nested=True` argument for all tqdm instantiations except the **outermost**
bar. Here's an example:

.. code:: python

    from tqdm import trange
    from time import sleep

    for i in trange(10, desc='1st loop', leave=True):
        for j in trange(5, desc='2nd loop', leave=True, nested=True):
            for k in trange(100, desc='3nd loop', leave=True, nested=True):
                sleep(0.01)

On Windows `colorama <https://github.com/tartley/colorama>`__ will be used if
available to produce a beautiful nested display.


How to make a good progress bar
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A good progress bar is a useful progress bar. To be useful, ``tqdm`` displays
statistics and uses smart algorithms to predict and automagically adapt to
a variety of use cases with no or minimal configuration.

However, there is one thing that ``tqdm`` cannot do: choose a pertinent
progress indicator. To display a useful progress bar, it is very important that
you ensure that you supply ``tqdm`` with the most pertinent progress indicator,
which will reflect most accurately the current state of your program.
Usually, a good way is to preprocess quickly to first evaluate the total amount
of work to do before beginning the real processing.

To illustrate the importance of a good progress indicator, let's take the
following example: you want to walk through all files of a directory and
process their contents to do your biddings.

Here is a basic program to do that:

.. code:: python

    import os
    from tqdm import tqdm, trange
    from time import sleep

    def dosomething(buf):
        """Do something with the content of a file"""
        sleep(0.01)
        pass

    def walkdir(folder):
        """Walk through each files in a directory"""
        for dirpath, dirs, files in os.walk(folder):
            for filename in files:
                yield os.path.abspath(os.path.join(dirpath, filename))

    def process_content_no_progress(inputpath, blocksize=1024):
        for filepath in walkdir(inputpath):
            with open(filepath, 'rb') as fh:
                buf = 1
                while (buf):
                    buf = fh.read(blocksize)
                    dosomething(buf)

``process_content_no_progress()`` does the job alright, but it does not show
any information about the current progress, nor how long it will take.

To quickly fix that using ``tqdm``, we can use this naive approach:

.. code:: python

    def process_content_with_progress1(inputpath, blocksize=1024):
        for filepath in tqdm(walkdir(inputpath), leave=True):
            with open(filepath, 'rb') as fh:
                buf = 1
                while (buf):
                    buf = fh.read(blocksize)
                    dosomething(buf)

``process_content_with_progress1()`` will load ``tqdm()``, but since the
iterator does not provide any length (``os.walkdir()`` does not have a
``__len__()`` method for the total files count), there is only an indication
of the current and past program state, no prediction:

``4it [00:03,  2.79it/s]``

The way to get predictive information is to know the total amount of work to be
done. Since ``os.walkdir()`` cannot give us this information, we need to
precompute this by ourselves:

.. code:: python

    def process_content_with_progress2(inputpath, blocksize=1024):
        # Preprocess the total files count
        filecounter = 0
        for dirpath, dirs, files in tqdm(os.walk(inputpath)):
            for filename in files:
                filecounter += 1

        for filepath in tqdm(walkdir(inputpath), total=filecounter, leave=True):
            with open(filepath, 'rb') as fh:
                buf = 1
                while (buf):
                    buf = fh.read(blocksize)
                    dosomething(buf)

``process_content_with_progress2()`` is better than the naive approach because
now we have predictive information:

50%|██████████████████████\                      \| 2/4 [00:00<00:00,  4.06it/s]

However, the progress is not smooth: it increments in steps, 1 step being
1 file processed. The problem is that we do not just walk through files tree,
but we process the files contents. Thus, if we stumble on one big fat file,
it will take a huge deal more time to process than other smaller files, but
the progress bar cannot know that, because we only supplied the files count,
so it considers that every element is of equal processing weight.

To fix this, we should use another indicator than the files count: the total
sum of all files sizes. This would be more pertinent since the data we
process is the files' content, so there is a direct relation between size and
content.

Below we implement this approach using a manually updated ``tqdm`` bar, where
``tqdm`` will work on size, while the ``for`` loop works on files paths:

.. code:: python

    def process_content_with_progress3(inputpath, blocksize=1024):
        # Preprocess the total files sizes
        sizecounter = 0
        for dirpath, dirs, files in tqdm(os.walk(inputpath)):
            for filename in files:
                fullpath = os.path.abspath(os.path.join(dirpath, filename))
                sizecounter += os.stat(fullpath).st_size 

        # Load tqdm with size counter instead of files counter
        with tqdm(total=sizecounter, leave=True, unit='B', unit_scale=True) as pbar:
            for dirpath, dirs, files in os.walk(inputpath):
                for filename in files:
                    fullpath = os.path.abspath(os.path.join(dirpath, filename))
                    with open(fullpath, 'rb') as fh:
                        buf = 1
                        while (buf):
                            buf = fh.read(blocksize)
                            dosomething(buf)
                            if buf: pbar.update(len(buf))

And here is the result: a much smoother progress bar with meaningful
predicted time and statistics:

47%|██████████████████▍\                    \| 152K/321K [00:03<00:03, 46.2KB/s]

Contributions
-------------

To run the testing suite please make sure tox (https://testrun.org/tox/latest/)
is installed, then type ``tox`` from the command line.

Where ``tox`` is unavailable, a Makefile-like setup is
provided with the following command:

.. code:: sh

    $ python setup.py make alltests

To see all options, run:

.. code:: sh

    $ python setup.py make

See the `CONTRIBUTE <https://raw.githubusercontent.com/tqdm/tqdm/master/CONTRIBUTE>`__
file for more information.


License
-------

`MIT LICENSE <https://raw.githubusercontent.com/tqdm/tqdm/master/LICENSE>`__.


Authors
-------

-  Casper da Costa-Luis (casperdcl)
-  Stephen Larroque (lrq3000)
-  Hadrien Mary (hadim)
-  Noam Yorav-Raphael (noamraph)*
-  Ivan Ivanov (obiwanus)
-  Mikhail Korobov (kmike)

`*` Original author

.. |Logo| image:: https://raw.githubusercontent.com/tqdm/tqdm/master/logo.png
.. |Build Status| image:: https://travis-ci.org/tqdm/tqdm.svg?branch=master
   :target: https://travis-ci.org/tqdm/tqdm
.. |Coverage Status| image:: https://coveralls.io/repos/tqdm/tqdm/badge.svg
   :target: https://coveralls.io/r/tqdm/tqdm
.. |Branch Coverage Status| image:: https://codecov.io/github/tqdm/tqdm/coverage.svg?branch=master
   :target: https://codecov.io/github/tqdm/tqdm?branch=master
.. |PyPi Status| image:: https://img.shields.io/pypi/v/tqdm.svg
   :target: https://pypi.python.org/pypi/tqdm
.. |PyPi Downloads| image:: https://img.shields.io/pypi/dm/tqdm.svg
   :target: https://pypi.python.org/pypi/tqdm
.. |Screenshot| image:: https://raw.githubusercontent.com/tqdm/tqdm/master/tqdm.gif
