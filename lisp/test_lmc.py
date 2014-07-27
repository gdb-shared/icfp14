import lmc
import io

def testme():
    assert 1
def test_Blocks():
    g = lmc.Blocks()
    g.AddMain(['I am main'])
    g.Add(['line1', 'line2'])
    s = io.BytesIO()
    g.Print(s)
    #assert s.get() == ''
