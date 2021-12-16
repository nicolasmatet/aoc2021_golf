import unittest

from j16.solve import Paquet, BinStream


class Test(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test1(self):
        bin_stream = BinStream('8A004A801A8002F478')
        paquet = Paquet.parse_paquet_hierarchy(bin_stream)
        self.assertEqual(paquet.sum_versions(), 16)

    def test2(self):
        bin_stream = BinStream('620080001611562C8802118E34')
        paquet = Paquet.parse_paquet_hierarchy(bin_stream)
        self.assertEqual(paquet.sum_versions(), 12)

    def test3(self):
        bin_stream = BinStream('C0015000016115A2E0802F182340')
        paquet = Paquet.parse_paquet_hierarchy(bin_stream)
        self.assertEqual(paquet.sum_versions(), 23)

    def test4(self):
        bin_stream = BinStream('A0016C880162017C3686B18A3D4780')
        paquet = Paquet.parse_paquet_hierarchy(bin_stream)
        self.assertEqual(paquet.sum_versions(), 31)

    def test_evaluate1(self):
        bin_stream = BinStream('C200B40A82')
        paquet = Paquet.parse_paquet_hierarchy(bin_stream)
        self.assertEqual(paquet.evaluate(), 3)

    def test_evaluate2(self):
        bin_stream = BinStream('04005AC33890')
        paquet = Paquet.parse_paquet_hierarchy(bin_stream)
        self.assertEqual(paquet.evaluate(), 54)

    def test_evaluate3(self):
        bin_stream = BinStream('880086C3E88112')
        paquet = Paquet.parse_paquet_hierarchy(bin_stream)
        self.assertEqual(paquet.evaluate(), 7)

    def test_evaluate4(self):
        bin_stream = BinStream('CE00C43D881120')
        paquet = Paquet.parse_paquet_hierarchy(bin_stream)
        self.assertEqual(paquet.evaluate(), 9)

    def test_evaluate5(self):
        bin_stream = BinStream('D8005AC2A8F0')
        paquet = Paquet.parse_paquet_hierarchy(bin_stream)
        self.assertEqual(paquet.evaluate(), 1)

    def test_evaluate6(self):
        bin_stream = BinStream('F600BC2D8F')
        paquet = Paquet.parse_paquet_hierarchy(bin_stream)
        self.assertEqual(paquet.evaluate(), 0)

    def test_evaluate7(self):
        bin_stream = BinStream('9C005AC2F8F0')
        paquet = Paquet.parse_paquet_hierarchy(bin_stream)
        self.assertEqual(paquet.evaluate(), 0)

    def test_evaluate8(self):
        bin_stream = BinStream('9C0141080250320F1802104A08')
        paquet = Paquet.parse_paquet_hierarchy(bin_stream)
        self.assertEqual(paquet.evaluate(), 1)


if __name__ == '__main__':
    unittest.main()
