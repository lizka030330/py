import random
import string
import unittest

def generate_password(length):
    if length <= 0:
        raise ValueError("Довжина пароля має бути більшою за нуль.")
    
    all_characters = string.ascii_letters + string.digits + string.punctuation
    password = random.choices(all_characters, k=length)
    random.shuffle(password)
    return ''.join(password)

class TestPasswordGeneration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.password = generate_password(12)
        print(f"Згенерований пароль: {cls.password}")  

    def test_password_length(self):
        self.assertEqual(len(self.password), 12, f"Пароль має бути довжиною 12, але отримано {len(self.password)}")
    
    def test_password_content(self):
        self.assertTrue(any(c.isdigit() for c in self.password), "Пароль повинен містити цифри")
        self.assertTrue(any(c.isalpha() for c in self.password), "Пароль повинен містити літери")
        self.assertTrue(any(c in string.punctuation for c in self.password), "Пароль повинен містити спеціальні символи")
    
    def test_invalid_length(self):
        with self.assertRaises(ValueError):
            generate_password(0)
        
        with self.assertRaises(ValueError):
            generate_password(-1)

if __name__ == "__main__":
    unittest.main()
