import lmc
import io

def testme():
    assert 1
def test_Blocks():
    g = lmc.Blocks()
    label = g.Add(['line1', 'line2'])
    g.AddMain(['I am main ' + label])
    s = io.BytesIO()
    g.Print(s, with_linenos=False)
    expected = '''\
  I am main 1
  line1
  line2
'''
    assert s.getvalue() == expected
