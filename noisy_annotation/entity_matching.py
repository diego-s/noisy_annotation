from flashtext import KeywordProcessor


class Entity(object):
    
    """A data structure to represent an entity and its metadata.
    
    :param entity_id: An identifier for the entity.
    :type entity_id: int
    :param entity_type: The type of entity.
    :type entity_type: str
    :param synonyms: A list of synonyms of this entity (the first synonym is 
        the preferred term).
    :type synonyms: list
    """

    def __init__(self, 
        entity_id, 
        synonyms, 
        entity_type, 
   ):
        self.entity_id = entity_id
        self.synonyms = synonyms
        self.entity_type = entity_type


class EntityMatch(object):
    
    """A data structure for entity matches.
    
    :param entity: The matched entity.
    :type entity: Entity
    :param start: The starting character of the match.
    :type start: int
    :param end: The ending character of the match.
    :type end: int
    :param substring: The matched substring.
    :type substring: str
    :param snippet: A snippet showing the match in context.
    :type snippet: str
    """

    def __init__(self, 
        entity, 
        start, 
        end, 
        substring, 
        snippet, 
   ):
        self.entity = entity
        self.start = start
        self.end = end
        self.substring = substring
        self.snippet = snippet
    
 
class EntityMatcher(object):
    
    """An object that can extract matches of entities in text.
    
    :param case_sensitive: Whether the entity matcher should be case sensitive, 
        defaults to False.
    :type case_sensitive: bool
    """

    def __init__(self, case_sensitive=False):
        self._keyword_processor = KeywordProcessor(
            case_sensitive=case_sensitive)
        self._synonym_id_map = {}
        self._id_entity_map = {}
        self._entity_ids = set()


    def add_entity(self, entity):
        
        """Add an entity to the matcher.

        :param entity: An Entity object to be added.
        :type entity: Entity
        """
        
        if self.has_id(entity.entity_id):
            raise KeyError("entity_id '%s' already seen before." % \
                entity.entity_id)
        self._entity_ids.add(entity.entity_id)
        self._id_entity_map[entity.entity_id] = entity
        for synonym in entity.synonyms:
            if synonym not in self._synonym_id_map.keys():
                self._synonym_id_map[synonym] = set()
            self._synonym_id_map[synonym].add(entity.entity_id)
            self._keyword_processor.add_keyword(synonym)


    def _get_snippet(self, text, start, end):
        snippet = ""
        snippet_start = max(0, start - 50)
        if snippet_start > 0:
            snippet += "..."
        snippet_end = min(len(text), end + 50)
        snippet += text[snippet_start:start] + "**" + text[start:end].upper() \
            + "**" + text[end:snippet_end]
        if snippet_end < len(text):
            snippet += "..."
        return snippet

            
    def get_matches(self, text):
        
        """Get a list of matches from text.
        
        :param text: A text to extract matches from.
        :type text: str
        
        :return: A list of EntityMatch objects extracted from the text.
        :type: list
        """
        
        matches = []
        keyword_matches = self._keyword_processor.extract_keywords(text, 
            span_info=True)
        for keyword_match, start, end in keyword_matches:
            entity_ids = self._synonym_id_map[keyword_match]
            for entity_id in entity_ids:
                entity = self._id_entity_map[entity_id]
                substring = text[start:end]
                snippet = self._get_snippet(text, start, end)
                match = EntityMatch(entity, start, end, substring, snippet)
                matches.append(match)
        return matches


    def has_id(self, entity_id):
        
        """Returns true if the entity_id is already present in the matcher.

        :param entity_id: An entity_id string.
        :type entity_id: str
        
        :return: True if the entity_id is already present in the matcher.
        :rtype: bool
        """
        
        return entity_id in self._entity_ids
