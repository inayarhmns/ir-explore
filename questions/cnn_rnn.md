- why does cnn need padding?


Convolutional filters only apply to the areas of an image within their receptive field, meaning the borders receive less attention.
With padding, the filters can cover more of the border area, allowing the network to learn patterns closer to the edges.
This improves feature extraction for objects near the edges of images and helps prevent loss of information along the borders.