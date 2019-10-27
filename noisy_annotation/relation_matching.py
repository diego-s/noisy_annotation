from noisy_annotation.entity_matching import EntityMatcher


class Relation(object):
    
    """A data structure representing a relation between entities and its 
    metadata.

    :param relation_id: An identifier for the relation.
    :type relation_id: str
    :param entities: A list of entities.
    :type entities: list
    """

    def __init__(self, 
        relation_id, 
        entities, 
    ):
        self.relation_id = relation_id
        self.entities = entities
    
    
class RelationMatch(object):
    
    """A data structure for relation matches.
    
    :param entity_matches: A list of EntityMatch objects.
    :type entity_matches: list
    :param snippet: A snippet string.
    :type snippet: str
    """

    def __init__(self, 
        entity_matches, 
        snippet
    ):
        self.entity_matches = entity_matches
        self.snippet = snippet


class RelationMatcher(object):
    
    """A matcher to extract relations found in text."""
    

    def __init__(self):
        self.entity_matcher = EntityMatcher()
        self._relations = []
        self._relation_dict = {}
        self._relation_ids = set()


    def _get_entity_match_dict(self, entity_matches):
        entity_match_dict = {}
        for entity_match in entity_matches:
            entity_id = entity_match.entity.entity_id
            if entity_id not in entity_match_dict.keys():
                entity_match_dict[entity_id] = set()
            entity_match_dict[entity_id].add(entity_match)
        return entity_match_dict


    def _highlight_text(self, text, entity_matches):
        offset = 0
        entity_matches = sorted(entity_matches, key=lambda m: m.start)
        for entity_match in entity_matches:
            start = entity_match.start + offset
            end = entity_match.end + offset
            text = text[:start] + "**" + text[start:end].upper() + "**" + \
                text[end:]
            offset += 4
        return text
        
        
    def _get_snippet(self, text, entity_matches):
        text = self._highlight_text(text, entity_matches)
        snippet = ""
        snippet_start = max(0, min([e.start for e in entity_matches]) - 50)
        if snippet_start > 0:
            snippet += "..."
        snippet_end = min(len(text), max([e.end for e in entity_matches]) + 50)
        snippet += text[snippet_start:snippet_end]
        if snippet_end < len(text):
            snippet += "..."
        return snippet


    def _get_relation_match(self, text, entity_matches, max_span):
        if max_span != None:
            min_position = min([m.end for m in entity_matches])
            max_position = max([m.start for m in entity_matches])
            if max_position - min_position > max_span:
                return None
        snippet = self._get_snippet(text, entity_matches)
        relation_match = RelationMatch(
            entity_matches, 
            snippet, 
        )
        return relation_match


    def _to_relation_matches(self, text, match_list_tuples, max_span):
        relation_matches = []
        for match_list_tuple in match_list_tuples:
            entity_matches_list = [[m] for m in match_list_tuple[0]]
            for i in range(1, len(match_list_tuple)):
                entity_matches_list = [t + [m] for m in match_list_tuple[i] \
                    for t in entity_matches_list]
            for entity_matches in entity_matches_list:
                relation_match = self._get_relation_match(text, entity_matches, 
                    max_span)
                if relation_match != None:
                    relation_matches.append(relation_match)
        return relation_matches


    def _get_matching_relations(self, entity_matches):
        matching_relations = set()
        for entity_match in entity_matches:
            entity_id = entity_match.entity.entity_id
            entity_relations = self._relation_dict.get(entity_id, None)
            if entity_relations != None:
                matching_relations = matching_relations.union(entity_relations)
        return matching_relations


    def _add_to_match_list(self, entity_match_dict, match_list_tuple, entities):
        miss = False
        for i in range(len(entities)):
            entity_id = entities[i].entity_id
            match_list = entity_match_dict.get(entity_id, None)
            if match_list != None:
                match_list_tuple.append(match_list)
            else:
                miss = True
                break
        return miss
        
        
    def add_relation(self, relation):
        
        """Add a relation to the matcher.

        :param relation: A Relation object.
        :type relation: Relation
        """
        
        if self.has_id(relation.relation_id):
            raise KeyError("relation_id '%s' already seen before." % \
                relation.relation_id)
        self._relation_ids.add(relation.relation_id)
        for entity in relation.entities:
            if not self.entity_matcher.has_id(entity.entity_id):
                self.entity_matcher.add_entity(entity)
        self._relations.append(relation)
        for entity in relation.entities:
            entity_id = entity.entity_id
            if entity_id not in self._relation_dict.keys():
                self._relation_dict[entity_id] = set()
            self._relation_dict[entity_id].add(relation)


    def get_matches(self, text, max_span=200):
        
        """Get a list of relation matches.
        
        :param text: A text to extract matches from.
        :type text: str
        :param max_span: The maximum span (in characters) between the first 
            and last entity match of the resulting relation matches. If a 
            relation match is found with a longer distance, it is discarded.
        :type max_span: int
        
        :return: A list of RelationMatch objects extracted from the text.
        :rtype: list
        """
        
        entity_matches = self.entity_matcher.get_matches(text)
        entity_match_dict = self._get_entity_match_dict(entity_matches)
        match_list_tuples = []
        relations = self._get_matching_relations(entity_matches)
        for relation in relations:
            match_list_tuple = []
            miss = self._add_to_match_list(entity_match_dict, match_list_tuple, 
                relation.entities)
            if not miss:
                match_list_tuples.append(match_list_tuple)
        relation_matches = self._to_relation_matches(text, match_list_tuples, 
            max_span)
        return relation_matches


    def has_id(self, relation_id):
        
        """Returns true if the relation_id is already present in the matcher.

        :param relation_id: An relation_id string.
        :type relation_id: str
        
        :return: True if the relation_id is already present in the matcher.
        :rtype: bool
        """
        
        return relation_id in self._relation_ids
