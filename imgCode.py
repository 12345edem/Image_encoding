from PIL import Image, ImageDraw, ImageFont
import math

#encode string to binary code
def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

#decode binary code to string 
def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\\0'
	
#encode binary code to image
def binary_to_image(code):
	code = list(code)
	width = len(code) 
	height = 200
	size = (width, height)
	image = Image.new("RGB", size)
	draw = ImageDraw.Draw(image)
	for i in range (width):
		for j in range (height):
			if(code[i] == '0'):
				draw.point((i, j), (0, 0, 0))
			else:
				draw.point((i, j), (255, 255, 255))
	image.save('binary_to_image.png', "PNG")

#decode binary code from image
def image_to_binary(filename):
	image = Image.open(filename)
	pix = image.load()
	string = ''
	for i in range(image.size[0]):
		if(pix[i, 0] == (255, 255, 255)):
			string += '1'
		else:
			string += '0'
	#print('\n\n' + string)
	string = text_from_bits(string)
	f = open("decode.txt", "w")
	f.write(string)
	f.close()

def binary_to_image_qr(code):
	code = list(code)
	width = math.ceil(math.sqrt(len(code)))
	height = width
	size = (width, height)
	image = Image.new("RGB", size)
	draw = ImageDraw.Draw(image)
	k = 0
	for i in range(width):
		for j in range(height):
			try:
				if(code[k] == '0'):
					draw.point((i, j), (0, 0, 0))
				else:
					draw.point((i, j), (255, 255, 255))
			except	IndexError:
				draw.point((i, j), (254, 254, 254))
			k += 1
	image.save('binary_to_image_qr.png', "PNG")

def image_to_binary_qr(filename):
	image = Image.open(filename)
	pix = image.load()
	string =""
	for i in range(image.size[0]):
		for j in range(image.size[0]):
			if(pix[i, j] == (255, 255, 255)):
				string += '1'
			elif(pix[i , j] == (0, 0, 0)):
				string += '0'
	string = text_from_bits(string)
	f = open('decode_qr.txt', "w")
	f.write(string)
	f.close()

def main():
	print('Введите название текствого файла для кодирования(с расширением): ')
	filename = input()
	file = open(filename, 'r')
	text = file.read()
	bite_code = (text_to_bits(text))
	print(len(bite_code))
	binary_to_image(bite_code)
	image_to_binary('binary_to_image.png')
	binary_to_image_qr(bite_code)
	image_to_binary_qr('binary_to_image_qr.png')

	getch = input()

if __name__ == '__main__':
	main()
