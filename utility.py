import random
import string
def generate_manufucture(size=6,chars=string.ascii_lowercase):
	return ''.join(random.choice(chars) for _ in range(size))

def smart_gen(instance,size=6):
	get_object=instance.__class__
	
	pass

