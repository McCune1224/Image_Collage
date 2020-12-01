import image_lib as image
import sys
import math
import random


def makeGrayscale(originalImage, h, w):
    editedImage = originalImage.copy()

    # go through each pixel
    for x in range(width):
        for y in range(height):

            # get the current pixel's color
            pixel = originalImage.getPixel(x, y)
            r = pixel.getRed()
            g = pixel.getGreen()
            b = pixel.getBlue()

    # If the pixel color is not "sufficiently purple"
    # then make it black and white
            if not (b > g and r > g and b > r // 1.5):
                # get the average intensity of the three pixel colors
                avg = (r + g + b) // 3
                r = g = b = avg
                pixel = image.Pixel(r, g, b)

            # Write the new pixel to the new image
            editedImage.setPixel(x, y, pixel)
    try:
        editedImage.setPosition(h, w)
        return editedImage
    except:
        print("Invalid height and/or width")

# This takes a fourth argument, color, which lets the user choose what color they want to see on the screen
# Color is randomly selected if user doesn't pass a color.


def makeOneColor(originalImage, color, h, w):
    randomizer = 0
    if color == "random":
        randomizer = random.randint(1, 3)
    editedImage = originalImage.copy()
    for x in range(width):
        for y in range(height):
            pixel = originalImage.getPixel(x, y)
            if color == "red" or randomizer == 1:
                r = pixel.getRed()
                g = 0
                b = 0
            elif color == "blue" or randomizer == 2:
                r = 0
                g = 0
                b = pixel.getBlue()
            elif color == "green" or randomizer == 3:
                pixel = originalImage.getPixel(x, y)
                r = 0
                g = pixel.getGreen()
                b = 0

            newPixel = image.Pixel(r, g, b)

            # Write the new pixel to the new image
            editedImage.setPixel(x, y, newPixel)
    try:
        editedImage.setPosition(h, w)
        return editedImage
    except:
        print("Invalid height and/or width")


def makeHorizontalMirror(originalImage, h, w):
    editedImage = originalImage.copy()
    # get the edge pixel's value and go one less
    maxPos = width - 1
    for x in range(width):
        for y in range(height):
            # grab the pixel from the other side of the image
            oldPix = editedImage.getPixel(maxPos-x, y)
            # make that pixel the new current one
            editedImage.setPixel(x, y, oldPix)
    try:
        editedImage.setPosition(h, w)
        return editedImage
    except:
        print("Invalid height and/or width")


def makeHorizontalFlip(originalImage, h, w):
    last = width-1
    # same process for horizontal mirror, but we start with an empty image intsead of a copy
    editedImage = image.EmptyImage(width, height)
    for x in range(width):
        for y in range(height):
            pixel = originalImage.getPixel(last-x, y)
            editedImage.setPixel(x, y, pixel)
    try:
        editedImage.setPosition(h, w)
        return editedImage
    except:
        print("Invalid height and/or width")

# goes through each pixel in the image and does the rgb function we want, _sepiaTransform


def _pixelMapper(passedImage, rgbFunction):

    width = passedImage.getWidth()
    height = passedImage.getHeight()
    newIm = image.EmptyImage(width, height)

    for row in range(height):
        for col in range(width):
            pixel = passedImage.getPixel(col, row)
            newIm.setPixel(col, row, rgbFunction(pixel))
    return newIm

# pass in the image you want, and the method you want to alter the pixel, in our case _sepiaTransform


def _imageTransformation(passedImage, rgbFunction):
    width = passedImage.getWidth()
    height = passedImage.getHeight()
    return _pixelMapper(passedImage, rgbFunction)

# the values used to make the sepia filter image


def _sepiaTransform(old):
    r = old.getRed()
    g = old.getGreen()
    b = old.getBlue()
    newR = (r * .393 + g * .769 + b * .189)
    newR = min(int(newR), 255)

    newG = (r * .349 + g * .686 + b * .168)
    newG = min(int(newG), 255)

    newB = (r * .272 + g * .534 + b * .131)
    newB = min(int(newB), 255)
    return image.Pixel(newR, newG, newB)


def makeSepia(originalImage, h, w):
    # for this I used the function passing method we learned in class, the real work is done in _sepiaTransform
    editedImage = _imageTransformation(originalImage, _sepiaTransform)
    try:
        editedImage.setPosition(h, w)
        return editedImage
    except:
        print("Invalid height and/or width")


def _negativePixel(pixel):
    # get the RGB of each pixel, and then inverse it (-255).
    red = 255 - pixel.getRed()
    blue = 255 - pixel.getBlue()
    green = 255 - pixel.getGreen()
    return image.Pixel(red, blue, green)


def makeNegative(originalImage, h, w):
    # Count through the image, and for each pixel preform the _negativePixel transformation
    editedImage = originalImage.copy()
    for x in range(height):
        for y in range(width):
            negPix = _negativePixel(editedImage.getPixel(y, x))
            editedImage.setPixel(y, x, negPix)
    try:
        editedImage.setPosition(h, w)
        return editedImage
    except:
        print("Invalid height and/or width")


def _convolve(passedImage, pRow, pCol, kernel):
    kernelColBase = pCol-1
    kernelRowBase = pRow-1

    sum = 0
    # using a 3x3 grid method to count the kernel we are in, calculate the sum
    # based off the currenty pixel's red value times the kernel value we are at
    for row in range(kernelRowBase, kernelRowBase+3):
        for col in range(kernelColBase, kernelColBase+3):
            kColIndex = col-kernelColBase
            kRowIndex = row-kernelRowBase

        # xMask = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]
        # yMask = [[1, 0, -1], [2, 0, -2], [1, 0, -1]]

        pixel = passedImage.getPixel(col, row)
        intensity = pixel.getRed()
        sum = sum + intensity * kernel[kRowIndex][kColIndex]

    return sum


def makeEdgeDetect(originalImage, h, w):

    grayscaleImage = makeGrayscale(originalImage, h, w)

    editedImage = image.EmptyImage(
        originalImage.getWidth(), originalImage.getHeight())

    black = image.Pixel(0, 0, 0)
    white = image.Pixel(255, 255, 255)

    xMask = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]
    yMask = [[1, 0, -1], [2, 0, -2], [1, 0, -1]]

    # count through every pixel except the border pixels...
    for row in range(1, grayscaleImage.getHeight()-1):
        for col in range(1, grayscaleImage.getWidth()-1):
            gX = _convolve(grayscaleImage, row, col, xMask)
            gY = _convolve(grayscaleImage, row, col, yMask)
            g = math.sqrt(gX**2 + gY**2)
            # based off the values we get from squaring the gX and gY values from _convolve, set the pixel to black or white
            if g > 175:
                editedImage.setPixel(col, row, black)
            else:
                editedImage.setPixel(col, row, white)
    try:
        editedImage.setPosition(h, w)
        return editedImage
    except:
        print("Invalid height and/or width")


def _blurConvolve(passedImage, pRow, pCol, kernel):
    kernelColBase = pCol-1
    kernelRowBase = pRow-1
    r = 0
    g = 0
    b = 0
    # similar previous Convolve method, but the math being done here is based off a different single kernel
    # and tallys up the rgb values within the 3x3 grid, sum up the values, divide them by 13, and then return
    for row in range(kernelRowBase, kernelRowBase+3):
        for col in range(kernelColBase, kernelColBase+3):
            kColIndex = col-kernelColBase
            kRowIndex = row-kernelRowBase
            pixel = passedImage.getPixel(col, row)

            r += kernel[kRowIndex][kColIndex] * pixel.getRed()

            g += kernel[kRowIndex][kColIndex] * pixel.getGreen()

            b += kernel[kRowIndex][kColIndex] * pixel.getBlue()

    r = r//13
    g = g//13
    b = b//13
    # return all of the rgb values divided by 13 (floor division)
    return [r, g, b]


def makeBlurred(originalImage, h, w):
    editedImage = originalImage.copy()
    kmask = [[1, 2, 1], [2, 1, 2], [1, 2, 1]]

    #Count through the pixels besides the edge pixels
    for row in range(1, originalImage.getHeight()-1):
        for col in range(1, originalImage.getWidth()-1):

            rgbVals = _blurConvolve(originalImage, row, col, kmask)
            newPix = image.Pixel(rgbVals[0], rgbVals[1], rgbVals[2])
            editedImage.setPixel(col, row, newPix)

    try:
        editedImage.setPosition(h, w)
        return editedImage
    except:
        print("Invalid height and/or width")

#So in all honesty I was attempting to make a sharpen image from a kernel I found form
#The kernel image processing wiki https://en.wikipedia.org/wiki/Kernel_(image_processing)
#But I was messing around with the numbers and got this somewhat infared filter to work?
def _InfaredConvolve(passedImage, pRow, pCol, kernel):
    kernelColBase = pCol-1
    kernelRowBase = pRow-1
    r = 0
    g = 0
    b = 0
    # similar previous Convolve method, but the math being done here is based off a different single kernel
    # and tallys up the rgb values within the 3x3 grid, sum up the values, divide them by 13, and then return
    for row in range(kernelRowBase, kernelRowBase+3):
        for col in range(kernelColBase, kernelColBase+3):
            kColIndex = col-kernelColBase
            kRowIndex = row-kernelRowBase
            pixel = passedImage.getPixel(col, row)

            r += kernel[kRowIndex][kColIndex] * pixel.getRed()

            g += kernel[kRowIndex][kColIndex] * pixel.getGreen()

            b += kernel[kRowIndex][kColIndex] * pixel.getBlue()

            if r > 255 and r > 0:
                r = r//13
            if g > 255 and g > 0:
                g = g//13
            if b > 255 and b > 0:
                b = b//13

            if r < 0:
                r = 255+r
            if g < 0:
                g = 255+g
            if b < 0:
                b = 255+b
    return [r, g, b]


def makeInfared(originalImage, h, w):
    editedImage = originalImage.copy()
    kmask = [[0, -1, 0], [-1, 5, -1], [0, -1, 0]]

    # Count through the pixels besides the edge pixels
    for row in range(1, originalImage.getHeight()-1):
        for col in range(1, originalImage.getWidth()-1):

            rgbVals = _InfaredConvolve(originalImage, row, col, kmask)
            newPix = image.Pixel(rgbVals[0], rgbVals[1], rgbVals[2])
            editedImage.setPixel(col, row, newPix)

    try:
        editedImage.setPosition(h, w)
        return editedImage
    except:
        print("Invalid height and/or width")


if __name__ == '__main__':
    # Open the original image and get store dimensions in two variables

    originalImage = image.FileImage(sys.argv[1])

    width = originalImage.getWidth()
    height = originalImage.getHeight()
    #window for images to be displayed
    graphicsWindow = image.ImageWin(width * 3, height*3, "3x3 Grid")

    infaredImage = makeInfared(originalImage,width,height)
    infaredImage.draw(graphicsWindow)
    
    grayscaleImage = makeGrayscale(originalImage, 0, height)
    grayscaleImage.draw(graphicsWindow)
    
    mirroredImage = makeHorizontalMirror(originalImage, width*2, 0)
    mirroredImage.draw(graphicsWindow)

    negativeImage = makeNegative(originalImage, width*2, height)
    negativeImage.draw(graphicsWindow)

    sepiaImage = makeSepia(originalImage, width, 0)
    sepiaImage.draw(graphicsWindow)

    flippedImage = makeHorizontalFlip(originalImage, 0, 0)
    flippedImage.draw(graphicsWindow)

    try:
        print("selected color: " + sys.argv[2])
    except:
        sys.argv.append("random")

    singleColor = makeOneColor(originalImage, sys.argv[2], width, height*2)
    singleColor.draw(graphicsWindow)

    outlinedImage = makeEdgeDetect(originalImage, 0, height*2)
    outlinedImage.draw(graphicsWindow)

    blurredImage = makeBlurred(originalImage, width*2, height*2)
    blurredImage.draw(graphicsWindow)
    
    graphicsWindow.exitOnClick()

#I didn't make the save and I wont have time to work on that, but im presuming
#you just make an image the size of the graphics window, 
# enumerate by thirds of the screen's dimensions, then enumerate the height
#and width of a each image, get their pixels, and set them to one of the nine quadrants
# of the screen... 
    infaredImage.save("infared.png")