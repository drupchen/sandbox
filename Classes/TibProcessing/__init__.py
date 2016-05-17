import os
import json
this_dir, this_filename = os.path.split(__file__)

# lexicon used by Segment()
with open(os.path.join(this_dir, "data", "lexicon.txt"), 'r', -1, 'utf-8-sig') as f:
    lexicon = [line.strip() for line in f.readlines()]
with open(os.path.join(this_dir, "data", "monlam1_verbs.txt"), 'r', -1, 'utf-8-sig') as f:
    monlam_verbs = [line.strip().split(' | ')[0] for line in f.readlines()]
with open(os.path.join(this_dir, "data", "particles.json"), 'r', -1, 'utf-8-sig') as f:
    particles = json.loads(f.read())['particles']
lexicon.extend(monlam_verbs)
lexicon.extend(particles)

# data for SylComponents()
with open(os.path.join(this_dir, "data", "syl_components.json"), 'r', -1, 'utf-8-sig') as f:
    data = json.loads(f.read())
dadrag = data['dadrag']
roots = data['roots']
suffixes = data['suffixes']
Csuffixes = data['Csuffixes']
special = data['special']
wazurs = data['wazurs']
ambiguous = data['ambiguous']
m_roots = data['m_roots']
m_exceptions = data['m_exceptions']
m_wazurs = data['m_wazurs']
# hack to turn lists to tuples as required for SylComponents
for am in ambiguous:
    ambiguous[am] = (ambiguous[am][0], ambiguous[am][1])

# data for Agreement
with open(os.path.join(this_dir, "data", "Agreement.json"), 'r', -1, 'utf-8-sig') as f:
    a_data = json.loads(f.read())
particles = a_data['particles']
corrections = a_data['corrections']


def SylComponents():
    from .SylComponents import SylComponents
    return SylComponents(dadrag, roots, suffixes, Csuffixes, special, wazurs, ambiguous, m_roots, m_exceptions, m_wazurs)


def Segment():
    from .Segmentation import Segment, strip_list, search
    SC = SylComponents()
    return Segment(lexicon, SC)


def Agreement():
    from .Agreement import Agreement
    return Agreement(particles, corrections)


__all__ = ['Segment', 'SylComponents', 'Agreement']