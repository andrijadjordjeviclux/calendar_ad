####################
# STRUCTURAL MODEL #
####################

from besser.BUML.metamodel.structural import (
    Class, Property, Method, Parameter,
    BinaryAssociation, Generalization, DomainModel,
    Enumeration, EnumerationLiteral, Multiplicity,
    StringType, IntegerType, FloatType, BooleanType,
    TimeType, DateType, DateTimeType, TimeDeltaType,
    AnyType, Constraint, AssociationClass, Metadata, MethodImplementationType
)

# Classes
Calendar = Class(name="Calendar")
Event = Class(name="Event")
Courses = Class(name="Courses")
Meeting = Class(name="Meeting")
Participant = Class(name="Participant")

# Calendar class attributes and methods
Calendar_Name: Property = Property(name="Name", type=StringType)
Calendar.attributes={Calendar_Name}

# Event class attributes and methods
Event_/numberEvents: Property = Property(name="/numberEvents", type=IntegerType, visibility="protected")
Event_Name: Property = Property(name="Name", type=StringType)
Event_Date: Property = Property(name="Date", type=DateType)
Event_Period: Property = Property(name="Period", type=TimeDeltaType)
Event_Place: Property = Property(name="Place", type=StringType)
Event.attributes={Event_/numberEvents, Event_Date, Event_Name, Event_Period, Event_Place}

# Courses class attributes and methods
Courses_Type: Property = Property(name="Type", type=StringType)
Courses.attributes={Courses_Type}

# Meeting class attributes and methods
Meeting_NumberParticipants: Property = Property(name="NumberParticipants", type=StringType)
Meeting.attributes={Meeting_NumberParticipants}

# Participant class attributes and methods
Participant_Name: Property = Property(name="Name", type=StringType)
Participant.attributes={Participant_Name}

# Relationships
Calendar_Event: BinaryAssociation = BinaryAssociation(
    name="Calendar_Event",
    ends={
        Property(name="calendar", type=Calendar, multiplicity=Multiplicity(1, 1)),
        Property(name="event", type=Event, multiplicity=Multiplicity(0, 9999))
    }
)
Participant_Meeting: BinaryAssociation = BinaryAssociation(
    name="Participant_Meeting",
    ends={
        Property(name="participant", type=Participant, multiplicity=Multiplicity(0, 9999)),
        Property(name="meeting", type=Meeting, multiplicity=Multiplicity(0, 9999))
    }
)

# Generalizations
gen_Courses_Event = Generalization(general=Event, specific=Courses)
gen_Meeting_Event = Generalization(general=Event, specific=Meeting)

# Domain Model
domain_model = DomainModel(
    name="Class_Diagram",
    types={Calendar, Event, Courses, Meeting, Participant},
    associations={Calendar_Event, Participant_Meeting},
    generalizations={gen_Courses_Event, gen_Meeting_Event},
    metadata=None
)
