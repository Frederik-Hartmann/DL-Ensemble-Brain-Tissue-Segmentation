# -----------------------------------------------------------------------------
# Multiresolution Unet file
# Author: Xavier Beltran Urbano and Frederik Hartmann
# Date Created: 12-01-2024
# -----------------------------------------------------------------------------


from .network import Network
from tensorflow.keras.layers import BatchNormalization, Conv2D, MaxPooling2D, Conv2DTranspose, concatenate
from tensorflow.keras import Model, Input

class MultiUnet(Network):
    def __init__(self, img_rows=256, img_cols=256, channels=3, classes=1):
        super().__init__(img_rows, img_cols, channels, classes)

    def get_model(self):
        inputs = Input((self.img_rows, self.img_cols, self.channels))

        conv1 = self.MultiConv2D(32, inputs)
        conv1 = BatchNormalization()(conv1)
        pool1 = MaxPooling2D(pool_size=(2, 2))(conv1)

        conv2 = self.MultiConv2D(64, pool1)
        conv2 = BatchNormalization()(conv2)
        pool2 = MaxPooling2D(pool_size=(2, 2))(conv2)

        conv3 = self.MultiConv2D(128, pool2)
        conv3 = BatchNormalization()(conv3)
        pool3 = MaxPooling2D(pool_size=(2, 2))(conv3)

        conv4 = self.MultiConv2D(256, pool3)
        conv4 = BatchNormalization()(conv4)

        up5 = concatenate([Conv2DTranspose(128, (2, 2), strides=(2, 2), padding='same', kernel_initializer='he_normal')(conv4), conv3], axis=3)
        conv5 = self.MultiConv2D(128, up5)
        conv5 = BatchNormalization()(conv5)

        up6 = concatenate([Conv2DTranspose(128, (2, 2), strides=(2, 2), padding='same', kernel_initializer='he_normal')(conv5), conv2], axis=3)
        conv6 = self.MultiConv2D(64, up6)
        conv6 = BatchNormalization()(conv6)

        up7 = concatenate([Conv2DTranspose(64, (2, 2), strides=(2, 2), padding='same', kernel_initializer='he_normal')(conv6), conv1], axis=3)
        conv7 = self.MultiConv2D(32, up7)
        conv7 = BatchNormalization()(conv7)

        if self.classes==1:
            conv_output = Conv2D(1, (1, 1), activation='sigmoid')(conv7)
        else:
            conv_output = Conv2D(self.classes, (1, 1), activation='softmax')(conv7)
        model = Model(inputs=inputs, outputs=conv_output)
        return model
