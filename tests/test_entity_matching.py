from noisy_annotation.entity_matching import Entity
from noisy_annotation.entity_matching import EntityMatcher


def test_entity_get_matches():
    text = "A mouse with Diabetes had Melanoma and PsA ans not PpsappA, diabetes or melanomas. It was given momilumab and Raspirin."
    matcher = EntityMatcher()
    entities = [
        Entity(1, ["diabetes"], "disease"), 
        Entity(2, ["melanoma"], "disease"), 
        Entity(3, ["psa"], "disease"), 
        Entity(4, ["momilumab"], "drug"), 
        Entity(5, ["raspirin"], "drug"), 
    ]
    for entity in entities:
        matcher.add_entity(entity)
    matches = matcher.get_matches(text)
    expected_num_matches = 6
    num_matches = len(matches)
    if num_matches != expected_num_matches:
        raise ValueError("Number of entity matches (%d) does not match the expected number of entity matches (%d)." % (num_matches, expected_num_matches))

def test_find_entities_by_synonym():
    matcher = EntityMatcher()
    entities = [
        Entity(1, ["diabetes"], "disease"), 
        Entity(2, ["melanoma"], "disease"), 
        Entity(3, ["psa"], "disease"), 
        Entity(4, ["momilumab"], "drug"), 
        Entity(5, ["raspirin"], "drug"), 
    ]
    for entity in entities:
        matcher.add_entity(entity)
    entities = matcher.find_entities_by_synonym("raspirin")
    assert entities == [entities[-1]]

def test_num_entities():
    matcher = EntityMatcher()
    entities = [
        Entity(1, ["diabetes"], "disease"), 
        Entity(2, ["melanoma"], "disease"), 
        Entity(3, ["psa"], "disease"), 
        Entity(4, ["momilumab"], "drug"), 
        Entity(5, ["raspirin"], "drug"), 
    ]
    for entity in entities:
        matcher.add_entity(entity)
    expected_num_entities = 5
    actual_num_entities = matcher.num_entities()
    assert actual_num_entities == expected_num_entities, \
        "Number of entities (%d) did not match expected number (%s)." % \
        (actual_num_entities, expected_num_entities)
