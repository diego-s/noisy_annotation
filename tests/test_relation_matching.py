from noisy_annotation.entity_matching import Entity
from noisy_annotation.entity_matching import EntityMatcher
from noisy_annotation.relation_matching import Relation
from noisy_annotation.relation_matching import RelationMatcher


def test_relation_get_matches():
    text = "A mouse with Diabetes had Melanoma and PsA ans not PpsappA, diabetes or melanomas. It was given momilumab and Raspirin."

    # Entity matching
    entities = [
        Entity(1, ["diabetes"], "disease"), 
        Entity(2, ["melanoma"], "disease"), 
        Entity(3, ["momilumab"], "drug"), 
        Entity(4, ["raspirin"], "drug"), 
    ]

    # Relation matching
    relations = [
        Relation(1, [entities[0], entities[2]]), 
        Relation(2, [entities[1], entities[3]]), 
    ]
    relation_matcher = RelationMatcher()
    for relation in relations:
        relation_matcher.add_relation(relation)

    # Test matching
    matches = relation_matcher.get_matches(text)
    for match in matches:
        print(match.snippet)
    expected_num_matches = 3
    num_matches = len(matches)
    if num_matches != expected_num_matches:
        raise ValueError("Number of relation matches (%d) does not match the expected number of relation matches (%d)." % (num_matches, expected_num_matches))
