# Hilbert Draw

## Library File

      HilbertDraw.py

## About

HilbertDraw is a library for drawing a version of an image using a
non-intersecting curve based on iterations approximating Hilbert's
Curve.

For example, consider the following drawing of the mathematician David
Hilbert.

![Drawing of David
 Hilbert](https://github.com/MatthewMcGonagle/HilbertDraw/blob/master/hilbertcartoon.png)

The output after processing this with HilbertDraw is

![HilbertDraw.py processing of Hilbert
 Drawing](https://github.com/MatthewMcGonagle/HilbertDraw/blob/master/Outputbw.png)

HilbertDraw.py works best with "cartoon-like" drawings that don't have
much detail. Furthermore, some pre-processing of colors may be
necessary. Small areas and fine details should be in darker
colors. Larger areas lacking detail may have lighter colors, depending
on preference.

## Implementation

The iterations for Hilbert's curve are created by recursively
subdividing rectangles into four equal rectangles. For example, for the
first three iterations, the number of rectangles are

1. one rectangle,
2. four rectangels,
3. 16 rectangles.

The curve for iteration **n** is constructed by putting an ordering on
the 4<sup>n-1</sup> rectangles of iteration **n**. This ordering depends on the
ordering for stage **n-1**. It is similar to an alphabetical
ordering. The earlier iteration orderings are stronger than the
ordering of the sub-divisions. For example, the ordering in stage 2 is
like the first letter of a word in the alphabet {a,b,c,d}. The
orderings for sub-division in stage 3 is like adding the second letter
from the alphabet {a,b,c,d}.

To render an image, the iterations are carried to different depths for
different parts of the image. This is implemented as a tree where each
node is one of the rectangles occurring in some stage the
iterations. The leaves are rectangles that will not be
sub-divided. The decision as to which rectangles should be sub-divided
is based on the level of color in the image. **Darker colors give more
sub-division**.

The curve is then generated by the lower-left corners of the
rectangles ordered as above.
