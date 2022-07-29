#
#  PreferencesPanelController.py
#  ControlledPreferences
#
#  Converted by u.fiedler on 04.02.05.
#  with great help from Bob Ippolito - Thank you Bob!
#
#  The original version was written in Objective-C by Malcolm Crawford
#  at http://homepage.mac.com/mmalc/CocoaExamples/controllers.html

import objc
from Cocoa import (
    NSArchiver,
    NSColor,
    NSFont,
    NSFontManager,
    NSUserDefaultsController,
    NSValueTransformer,
    NSWindowController,
)
from PyObjCTools.KeyValueCoding import getKey
from Cocoa import NSFont, NSString, NSValueTransformer
from PyObjCTools import AppHelper


class FontNameToDisplayNameTransformer(NSValueTransformer):
    """
    Takes as input the fontName of a font as stored in user defaults,
    returns the displayed font name of the font to show to the user.
    """

    @classmethod
    def transformedValueClass(cls):
        return NSString

    @classmethod
    def allowsReverseTransformation(cls):
        return False

    def transformedValue_(self, aValue):
        font = NSFont.fontWithName_size_(aValue, 12)
        return font.displayName()

from Cocoa import (
    NSAttributedString,
    NSDrawLightBezel,
    NSFont,
    NSFontAttributeName,
    NSInsetRect,
    NSMakePoint,
    NSNotificationCenter,
    NSRectFill,
    NSUnarchiver,
    NSUserDefaultsController,
    NSUserDefaultsDidChangeNotification,
    NSView,
)
from objc import super
from PyObjCTools.KeyValueCoding import getKey


class FontSampleDisplayView(NSView):
    """
    Display WordOfTheDay with the preferred font and color
    """

    def drawRect_(self, rect):
        defaults = NSUserDefaultsController.sharedUserDefaultsController().values()
        favoriteColor = NSUnarchiver.unarchiveObjectWithData_(
            getKey(defaults, "FavoriteColor")
        )
        fontName = getKey(defaults, "FontName")
        fontSize = getKey(defaults, "FontSize")
        favoriteFont = NSFont.fontWithName_size_(fontName, fontSize)
        wordOfTheDay = getKey(defaults, "WordOfTheDay")

        # Do the actual drawing
        myBounds = self.bounds()  # = (x, y), (bw, bh)
        NSDrawLightBezel(myBounds, myBounds)
        favoriteColor.set()
        NSRectFill(NSInsetRect(myBounds, 2, 2))
        attrsDictionary = {NSFontAttributeName: favoriteFont}
        attrString = NSAttributedString.alloc().initWithString_attributes_(
            wordOfTheDay, attrsDictionary
        )
        attrSize = attrString.size()  # = (bw, bh)
        attrString.drawAtPoint_(
            NSMakePoint(
                (attrSize.width / -2) + (myBounds.size.width / 2),
                (attrSize.height / -2) + (myBounds.size.height / 2),
            )
        )

    def initWithFrame_(self, frameRect):
        self = super().initWithFrame_(frameRect)
        dnc = NSNotificationCenter.defaultCenter()
        dnc.addObserver_selector_name_object_(
            self, "redisplay:", NSUserDefaultsDidChangeNotification, None
        )
        return self

    def redisplay_(self, sender):
        self.setNeedsDisplay_(True)

class PreferencesPanelController(NSWindowController):
    @objc.IBAction
    def changeTextFont_(self, sender):
        """The user changed the current font selection, so update the default font"""

        # Get font name and size from user defaults
        defaults = NSUserDefaultsController.sharedUserDefaultsController().values()
        fontName = getKey(defaults, "FontName")
        fontSize = getKey(defaults, "FontSize")

        # Create font from name and size; initialize font panel
        font = NSFont.fontWithName_size_(fontName, fontSize)
        if font is None:
            font = NSFont.systemFontOfSize_(NSFont.systemFontSize())
        NSFontManager.sharedFontManager().setSelectedFont_isMultiple_(font, False)
        NSFontManager.sharedFontManager().orderFrontFontPanel_(self)

        # Set window as firstResponder so we get changeFont: messages
        self.window().makeFirstResponder_(self.window())

    @objc.IBAction
    def changeFont_(self, sender):
        """This is the message the font panel sends when a new font is selected"""
        # Get selected font
        fontManager = NSFontManager.sharedFontManager()
        selectedFont = fontManager.selectedFont()
        if selectedFont is None:
            selectedFont = NSFont.systemFontOfSize_(NSFont.systemFontSize())
        panelFont = fontManager.convertFont_(selectedFont)

        # Get and store details of selected font
        # Note: use fontName, not displayName.  The font name identifies the font to
        # the system, we use a value transformer to show the user the display name
        fontSize = panelFont.pointSize()

        defaults = NSUserDefaultsController.sharedUserDefaultsController().values()
        defaults.setValue_forKey_(panelFont.fontName(), "FontName")
        defaults.setValue_forKey_(fontSize, "FontSize")


# Set up initial values for defaults:
# Create dictionary with keys and values for WordOfTheDay, FontName,
# FontSize, and FavoriteColor.  Mostly straightforward, but:
#
# Store the fontName of the font as the default; the textfield displays
# the font's displayName using a value transformer.
#
# The color must be archived -- you can't store NSColors directly in NSUserDefaults.
dictionary = {}
dictionary["WordOfTheDay"] = "Today"
systemFont = NSFont.systemFontOfSize_(NSFont.systemFontSize())
dictionary["FontName"] = systemFont.fontName()
dictionary["FontSize"] = systemFont.pointSize()
archivedColor = NSArchiver.archivedDataWithRootObject_(NSColor.greenColor())
dictionary["FavoriteColor"] = archivedColor
NSUserDefaultsController.sharedUserDefaultsController().setInitialValues_(dictionary)

# Create and register font name value transformer
transformer = FontNameToDisplayNameTransformer.alloc().init()
NSValueTransformer.setValueTransformer_forName_(
    transformer, "FontNameToDisplayNameTransformer"
)



# start the event loop
# AppHelper.runEventLoop()