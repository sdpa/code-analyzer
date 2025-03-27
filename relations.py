import enum

class RelationType(enum.Enum):
    # Syntactic Relations
    PARENT_OF = "ParentOf"
    CHILD_OF = "ChildOf"
    CONSTRUCTS = "Constructs"
    CONSTRUCTED_BY = "ConstructedBy"
    
    # Import Relations
    IMPORTS = "Imports"
    IMPORTED_BY = "ImportedBy"
    
    # Inheritance Relations
    BASE_CLASS_OF = "BaseClassOf"
    DERIVED_CLASS_OF = "DerivedClassOf"
    
    # Method Relations
    OVERRIDES = "Overrides"
    OVERRIDDEN_BY = "OverriddenBy"
    
    # Invocation Relations
    CALLS = "Calls"
    CALLED_BY = "CalledBy"
    
    # Instantiation Relations
    INSTANTIATES = "Instantiates"
    INSTANTIATED_BY = "InstantiatedBy"
    
    # Field Use Relations
    USES = "Uses"
    USED_BY = "UsedBy"