from ctypes import windll, byref, create_unicode_buffer, create_string_buffer
FR_PRIVATE = 0x10
FR_NOT_ENUM = 0x20

def add_font(fontpath: str, private = True, enumerable = False):
	if isinstance(fontpath, str):
		pathbuf = create_string_buffer(fontpath)
		AddFontResourceEx = windll.gdi32.AddFontResourceExA
	else:
		raise TypeError('fontpath must be of type str')
	flags = (FR_PRIVATE if private else 0) | (FR_NOT_ENUM if not enumerable else 0)
	numFontsAdded = AddFontResourceEx(byref(pathbuf), flags, 0)
	return bool(numFontsAdded)