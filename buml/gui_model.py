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


###############
#  GUI MODEL  #
###############

from besser.BUML.metamodel.gui import (
    GUIModel, Module, Screen,
    ViewComponent, ViewContainer,
    Button, ButtonType, ButtonActionType,
    Text, Image, Link, InputField, InputFieldType,
    Form, Menu, MenuItem, DataList,
    DataSource, DataSourceElement, EmbeddedContent,
    Styling, Size, Position, Color, Layout, LayoutType,
    UnitSize, PositionType, Alignment
)
from besser.BUML.metamodel.gui.dashboard import (
    LineChart, BarChart, PieChart, RadarChart, RadialBarChart, Table, AgentComponent,
    Column, FieldColumn, LookupColumn, ExpressionColumn, MetricCard, Series
)
from besser.BUML.metamodel.gui.events_actions import (
    Event, EventType, Transition, Create, Read, Update, Delete, Parameter
)
from besser.BUML.metamodel.gui.binding import DataBinding

# Module: GUI_Module

# Screen: wrapper
wrapper = Screen(name="wrapper", description="Calendar", view_elements=set(), is_main_page=True, route_path="/calendar", screen_size="Medium")
wrapper.component_id = "page-calendar-0"
igb1c = Text(
    name="igb1c",
    content="BESSER",
    description="Text element",
    styling=Styling(size=Size(font_size="24px", font_weight="bold", margin_top="0", margin_bottom="30px"), color=Color(color_palette="default")),
    component_id="igb1c",
    tag_name="h2",
    display_order=0,
    custom_attributes={"id": "igb1c"}
)
ijafe = Link(
    name="ijafe",
    description="Link element",
    label="Calendar",
    url="/calendar",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="rgba(255,255,255,0.2)", text_color="white", color_palette="default", border_radius="4px")),
    component_id="ijafe",
    tag_name="a",
    display_order=0,
    custom_attributes={"href": "/calendar", "id": "ijafe"}
)
ixw2j = Link(
    name="ixw2j",
    description="Link element",
    label="Event",
    url="/event",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="ixw2j",
    tag_name="a",
    display_order=1,
    custom_attributes={"href": "/event", "id": "ixw2j"}
)
i7ips = Link(
    name="i7ips",
    description="Link element",
    label="Category",
    url="/category",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="i7ips",
    tag_name="a",
    display_order=2,
    custom_attributes={"href": "/category", "id": "i7ips"}
)
ix4e6 = ViewContainer(
    name="ix4e6",
    description=" component",
    view_elements={ijafe, ixw2j, i7ips},
    styling=Styling(position=Position(display="flex"), color=Color(color_palette="default"), layout=Layout(layout_type=LayoutType.FLEX, flex_direction="column", flex="1")),
    component_id="ix4e6",
    display_order=1,
    custom_attributes={"id": "ix4e6"}
)
ix4e6_layout = Layout(layout_type=LayoutType.FLEX, flex_direction="column", flex="1")
ix4e6.layout = ix4e6_layout
iztgj = Text(
    name="iztgj",
    content="© 2026 BESSER. All rights reserved.",
    description="Text element",
    styling=Styling(size=Size(font_size="11px", padding_top="20px", margin_top="auto"), position=Position(alignment=Alignment.CENTER), color=Color(opacity="0.8", color_palette="default", border_top="1px solid rgba(255,255,255,0.2)")),
    component_id="iztgj",
    display_order=2,
    custom_attributes={"id": "iztgj"}
)
irel4 = ViewContainer(
    name="irel4",
    description="nav container",
    view_elements={igb1c, ix4e6, iztgj},
    styling=Styling(size=Size(width="250px", padding="20px", unit_size=UnitSize.PIXELS), position=Position(display="flex", overflow_y="auto"), color=Color(background_color="linear-gradient(135deg, #4b3c82 0%, #5a3d91 100%)", text_color="white", color_palette="default"), layout=Layout(layout_type=LayoutType.FLEX, flex_direction="column")),
    component_id="irel4",
    tag_name="nav",
    display_order=0,
    custom_attributes={"id": "irel4"}
)
irel4_layout = Layout(layout_type=LayoutType.FLEX, flex_direction="column")
irel4.layout = irel4_layout
idhxl = Text(
    name="idhxl",
    content="Calendar",
    description="Text element",
    styling=Styling(size=Size(font_size="32px", margin_top="0", margin_bottom="10px"), color=Color(text_color="#333", color_palette="default")),
    component_id="idhxl",
    tag_name="h1",
    display_order=0,
    custom_attributes={"id": "idhxl"}
)
irvr6 = Text(
    name="irvr6",
    content="Manage Calendar data",
    description="Text element",
    styling=Styling(size=Size(margin_bottom="30px"), color=Color(text_color="#666", color_palette="default")),
    component_id="irvr6",
    tag_name="p",
    display_order=1,
    custom_attributes={"id": "irvr6"}
)
table_calendar_0_col_0 = FieldColumn(label="Name", field=Calendar_Name)
table_calendar_0 = Table(
    name="table_calendar_0",
    title="Calendar List",
    primary_color="#2c3e50",
    show_header=True,
    striped_rows=False,
    show_pagination=True,
    rows_per_page=5,
    action_buttons=True,
    columns=[table_calendar_0_col_0],
    styling=Styling(size=Size(width="100%", min_height="400px", unit_size=UnitSize.PERCENTAGE), color=Color(color_palette="default", primary_color="#2c3e50")),
    component_id="table-calendar-0",
    display_order=2,
    custom_attributes={"chart-color": "#2c3e50", "chart-title": "Calendar List", "data-source": "e7b494c7-1008-4eb3-a4d0-b51f5d3db02f", "show-header": "true", "striped-rows": "false", "show-pagination": "true", "rows-per-page": "5", "action-buttons": "true", "columns": [{'field': 'Name', 'label': 'Name', 'columnType': 'field', '_expanded': False}, {'field': 'Event', 'label': 'Event', 'columnType': 'lookup', 'lookupEntity': '94cfdb19-a65f-4f32-893e-1d3e38c94131', 'lookupField': '/numberEvents', '_expanded': False}], "id": "table-calendar-0", "filter": ""}
)
domain_model_ref = globals().get('domain_model') or next((v for k, v in globals().items() if k.startswith('domain_model') and hasattr(v, 'get_class_by_name')), None)
table_calendar_0_binding_domain = None
if domain_model_ref is not None:
    table_calendar_0_binding_domain = domain_model_ref.get_class_by_name("Calendar")
if table_calendar_0_binding_domain:
    table_calendar_0_binding = DataBinding(domain_concept=table_calendar_0_binding_domain, name="CalendarDataBinding")
else:
    # Domain class 'Calendar' not resolved; data binding skipped.
    table_calendar_0_binding = None
if table_calendar_0_binding:
    table_calendar_0.data_binding = table_calendar_0_binding
ihn2f = ViewContainer(
    name="ihn2f",
    description="main container",
    view_elements={idhxl, irvr6, table_calendar_0},
    styling=Styling(size=Size(padding="40px"), position=Position(overflow_y="auto"), color=Color(background_color="#f5f5f5", color_palette="default"), layout=Layout(flex="1")),
    component_id="ihn2f",
    tag_name="main",
    display_order=1,
    custom_attributes={"id": "ihn2f"}
)
ihn2f_layout = Layout(flex="1")
ihn2f.layout = ihn2f_layout
i04xg = ViewContainer(
    name="i04xg",
    description=" component",
    view_elements={irel4, ihn2f},
    styling=Styling(size=Size(height="100vh", font_family="Arial, sans-serif"), position=Position(display="flex"), color=Color(color_palette="default"), layout=Layout(layout_type=LayoutType.FLEX)),
    component_id="i04xg",
    display_order=0,
    custom_attributes={"id": "i04xg"}
)
i04xg_layout = Layout(layout_type=LayoutType.FLEX)
i04xg.layout = i04xg_layout
wrapper.view_elements = {i04xg}


# Screen: wrapper_2
wrapper_2 = Screen(name="wrapper_2", description="Event", view_elements=set(), route_path="/event", screen_size="Medium")
wrapper_2.component_id = "page-event-1"
ihusg = Text(
    name="ihusg",
    content="BESSER",
    description="Text element",
    styling=Styling(size=Size(font_size="24px", font_weight="bold", margin_top="0", margin_bottom="30px"), color=Color(color_palette="default")),
    component_id="ihusg",
    tag_name="h2",
    display_order=0,
    custom_attributes={"id": "ihusg"}
)
iddsz = Link(
    name="iddsz",
    description="Link element",
    label="Calendar",
    url="/calendar",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="iddsz",
    tag_name="a",
    display_order=0,
    custom_attributes={"href": "/calendar", "id": "iddsz"}
)
ij8jj = Link(
    name="ij8jj",
    description="Link element",
    label="Event",
    url="/event",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="rgba(255,255,255,0.2)", text_color="white", color_palette="default", border_radius="4px")),
    component_id="ij8jj",
    tag_name="a",
    display_order=1,
    custom_attributes={"href": "/event", "id": "ij8jj"}
)
iq4w3 = Link(
    name="iq4w3",
    description="Link element",
    label="Category",
    url="/category",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="iq4w3",
    tag_name="a",
    display_order=2,
    custom_attributes={"href": "/category", "id": "iq4w3"}
)
inn6o = ViewContainer(
    name="inn6o",
    description=" component",
    view_elements={iddsz, ij8jj, iq4w3},
    styling=Styling(position=Position(display="flex"), color=Color(color_palette="default"), layout=Layout(layout_type=LayoutType.FLEX, flex_direction="column", flex="1")),
    component_id="inn6o",
    display_order=1,
    custom_attributes={"id": "inn6o"}
)
inn6o_layout = Layout(layout_type=LayoutType.FLEX, flex_direction="column", flex="1")
inn6o.layout = inn6o_layout
ifyvo = Text(
    name="ifyvo",
    content="© 2026 BESSER. All rights reserved.",
    description="Text element",
    styling=Styling(size=Size(font_size="11px", padding_top="20px", margin_top="auto"), position=Position(alignment=Alignment.CENTER), color=Color(opacity="0.8", color_palette="default", border_top="1px solid rgba(255,255,255,0.2)")),
    component_id="ifyvo",
    display_order=2,
    custom_attributes={"id": "ifyvo"}
)
iq1in = ViewContainer(
    name="iq1in",
    description="nav container",
    view_elements={ihusg, inn6o, ifyvo},
    styling=Styling(size=Size(width="250px", padding="20px", unit_size=UnitSize.PIXELS), position=Position(display="flex", overflow_y="auto"), color=Color(background_color="linear-gradient(135deg, #4b3c82 0%, #5a3d91 100%)", text_color="white", color_palette="default"), layout=Layout(layout_type=LayoutType.FLEX, flex_direction="column")),
    component_id="iq1in",
    tag_name="nav",
    display_order=0,
    custom_attributes={"id": "iq1in"}
)
iq1in_layout = Layout(layout_type=LayoutType.FLEX, flex_direction="column")
iq1in.layout = iq1in_layout
i4j2f = Text(
    name="i4j2f",
    content="Event",
    description="Text element",
    styling=Styling(size=Size(font_size="32px", margin_top="0", margin_bottom="10px"), color=Color(text_color="#333", color_palette="default")),
    component_id="i4j2f",
    tag_name="h1",
    display_order=0,
    custom_attributes={"id": "i4j2f"}
)
idfds = Text(
    name="idfds",
    content="Manage Event data",
    description="Text element",
    styling=Styling(size=Size(margin_bottom="30px"), color=Color(text_color="#666", color_palette="default")),
    component_id="idfds",
    tag_name="p",
    display_order=1,
    custom_attributes={"id": "idfds"}
)
table_event_1_col_0 = FieldColumn(label="/NumberEvents", field=Event_/numberEvents)
table_event_1_col_1 = FieldColumn(label="Name", field=Event_Name)
table_event_1_col_2 = FieldColumn(label="Date", field=Event_Date)
table_event_1_col_3 = FieldColumn(label="Period", field=Event_Period)
table_event_1 = Table(
    name="table_event_1",
    title="Event List",
    primary_color="#2c3e50",
    show_header=True,
    striped_rows=False,
    show_pagination=True,
    rows_per_page=5,
    action_buttons=True,
    columns=[table_event_1_col_0, table_event_1_col_1, table_event_1_col_2, table_event_1_col_3],
    styling=Styling(size=Size(width="100%", min_height="400px", unit_size=UnitSize.PERCENTAGE), color=Color(color_palette="default", primary_color="#2c3e50")),
    component_id="table-event-1",
    display_order=2,
    custom_attributes={"chart-color": "#2c3e50", "chart-title": "Event List", "data-source": "94cfdb19-a65f-4f32-893e-1d3e38c94131", "show-header": "true", "striped-rows": "false", "show-pagination": "true", "rows-per-page": "5", "action-buttons": "true", "columns": [{'field': '/numberEvents', 'label': '/NumberEvents', 'columnType': 'field', '_expanded': False}, {'field': 'Name', 'label': 'Name', 'columnType': 'field', '_expanded': False}, {'field': 'Date', 'label': 'Date', 'columnType': 'field', '_expanded': False}, {'field': 'Period', 'label': 'Period', 'columnType': 'field', '_expanded': False}, {'field': 'Calendar', 'label': 'Calendar', 'columnType': 'lookup', 'lookupEntity': 'e7b494c7-1008-4eb3-a4d0-b51f5d3db02f', 'lookupField': 'Name', '_expanded': False}, {'field': 'Category', 'label': 'Category', 'columnType': 'lookup', 'lookupEntity': 'ef0ee04b-ead2-4c76-bf30-ea0b022153dd', 'lookupField': 'Name', '_expanded': False}], "id": "table-event-1", "filter": ""}
)
domain_model_ref = globals().get('domain_model') or next((v for k, v in globals().items() if k.startswith('domain_model') and hasattr(v, 'get_class_by_name')), None)
table_event_1_binding_domain = None
if domain_model_ref is not None:
    table_event_1_binding_domain = domain_model_ref.get_class_by_name("Event")
if table_event_1_binding_domain:
    table_event_1_binding = DataBinding(domain_concept=table_event_1_binding_domain, name="EventDataBinding")
else:
    # Domain class 'Event' not resolved; data binding skipped.
    table_event_1_binding = None
if table_event_1_binding:
    table_event_1.data_binding = table_event_1_binding
ilx9t = ViewContainer(
    name="ilx9t",
    description="main container",
    view_elements={i4j2f, idfds, table_event_1},
    styling=Styling(size=Size(padding="40px"), position=Position(overflow_y="auto"), color=Color(background_color="#f5f5f5", color_palette="default"), layout=Layout(flex="1")),
    component_id="ilx9t",
    tag_name="main",
    display_order=1,
    custom_attributes={"id": "ilx9t"}
)
ilx9t_layout = Layout(flex="1")
ilx9t.layout = ilx9t_layout
iab1i = ViewContainer(
    name="iab1i",
    description=" component",
    view_elements={iq1in, ilx9t},
    styling=Styling(size=Size(height="100vh", font_family="Arial, sans-serif"), position=Position(display="flex"), color=Color(color_palette="default"), layout=Layout(layout_type=LayoutType.FLEX)),
    component_id="iab1i",
    display_order=0,
    custom_attributes={"id": "iab1i"}
)
iab1i_layout = Layout(layout_type=LayoutType.FLEX)
iab1i.layout = iab1i_layout
wrapper_2.view_elements = {iab1i}


# Screen: wrapper_3
wrapper_3 = Screen(name="wrapper_3", description="Category", view_elements=set(), route_path="/category", screen_size="Medium")
wrapper_3.component_id = "page-category-2"
i32ux = Text(
    name="i32ux",
    content="BESSER",
    description="Text element",
    styling=Styling(size=Size(font_size="24px", font_weight="bold", margin_top="0", margin_bottom="30px"), color=Color(color_palette="default")),
    component_id="i32ux",
    tag_name="h2",
    display_order=0,
    custom_attributes={"id": "i32ux"}
)
idfuc = Link(
    name="idfuc",
    description="Link element",
    label="Calendar",
    url="/calendar",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="idfuc",
    tag_name="a",
    display_order=0,
    custom_attributes={"href": "/calendar", "id": "idfuc"}
)
i2ys6 = Link(
    name="i2ys6",
    description="Link element",
    label="Event",
    url="/event",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="i2ys6",
    tag_name="a",
    display_order=1,
    custom_attributes={"href": "/event", "id": "i2ys6"}
)
ii1q5 = Link(
    name="ii1q5",
    description="Link element",
    label="Category",
    url="/category",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="rgba(255,255,255,0.2)", text_color="white", color_palette="default", border_radius="4px")),
    component_id="ii1q5",
    tag_name="a",
    display_order=2,
    custom_attributes={"href": "/category", "id": "ii1q5"}
)
i8suu = ViewContainer(
    name="i8suu",
    description=" component",
    view_elements={idfuc, i2ys6, ii1q5},
    styling=Styling(position=Position(display="flex"), color=Color(color_palette="default"), layout=Layout(layout_type=LayoutType.FLEX, flex_direction="column", flex="1")),
    component_id="i8suu",
    display_order=1,
    custom_attributes={"id": "i8suu"}
)
i8suu_layout = Layout(layout_type=LayoutType.FLEX, flex_direction="column", flex="1")
i8suu.layout = i8suu_layout
i5a1f = Text(
    name="i5a1f",
    content="© 2026 BESSER. All rights reserved.",
    description="Text element",
    styling=Styling(size=Size(font_size="11px", padding_top="20px", margin_top="auto"), position=Position(alignment=Alignment.CENTER), color=Color(opacity="0.8", color_palette="default", border_top="1px solid rgba(255,255,255,0.2)")),
    component_id="i5a1f",
    display_order=2,
    custom_attributes={"id": "i5a1f"}
)
inhjk = ViewContainer(
    name="inhjk",
    description="nav container",
    view_elements={i32ux, i8suu, i5a1f},
    styling=Styling(size=Size(width="250px", padding="20px", unit_size=UnitSize.PIXELS), position=Position(display="flex", overflow_y="auto"), color=Color(background_color="linear-gradient(135deg, #4b3c82 0%, #5a3d91 100%)", text_color="white", color_palette="default"), layout=Layout(layout_type=LayoutType.FLEX, flex_direction="column")),
    component_id="inhjk",
    tag_name="nav",
    display_order=0,
    custom_attributes={"id": "inhjk"}
)
inhjk_layout = Layout(layout_type=LayoutType.FLEX, flex_direction="column")
inhjk.layout = inhjk_layout
isgpg = Text(
    name="isgpg",
    content="Category",
    description="Text element",
    styling=Styling(size=Size(font_size="32px", margin_top="0", margin_bottom="10px"), color=Color(text_color="#333", color_palette="default")),
    component_id="isgpg",
    tag_name="h1",
    display_order=0,
    custom_attributes={"id": "isgpg"}
)
iufla = Text(
    name="iufla",
    content="Manage Category data",
    description="Text element",
    styling=Styling(size=Size(margin_bottom="30px"), color=Color(text_color="#666", color_palette="default")),
    component_id="iufla",
    tag_name="p",
    display_order=1,
    custom_attributes={"id": "iufla"}
)
table_category_2 = Table(
    name="table_category_2",
    title="Category List",
    primary_color="#2c3e50",
    show_header=True,
    striped_rows=False,
    show_pagination=True,
    rows_per_page=5,
    action_buttons=True,
    styling=Styling(size=Size(width="100%", min_height="400px", unit_size=UnitSize.PERCENTAGE), color=Color(color_palette="default", primary_color="#2c3e50")),
    component_id="table-category-2",
    display_order=2,
    css_classes=["has-data-binding"],
    custom_attributes={"chart-color": "#2c3e50", "chart-title": "Category List", "data-source": "ef0ee04b-ead2-4c76-bf30-ea0b022153dd", "show-header": "true", "striped-rows": "false", "show-pagination": "true", "rows-per-page": "5", "action-buttons": "true", "columns": [{'field': 'Name', 'label': 'Name', 'columnType': 'field', '_expanded': False}, {'field': 'Event', 'label': 'Event', 'columnType': 'lookup', 'lookupEntity': '94cfdb19-a65f-4f32-893e-1d3e38c94131', 'lookupField': '/numberEvents', '_expanded': False}], "id": "table-category-2", "filter": ""}
)
i114z = ViewContainer(
    name="i114z",
    description="main container",
    view_elements={isgpg, iufla, table_category_2},
    styling=Styling(size=Size(padding="40px"), position=Position(overflow_y="auto"), color=Color(background_color="#f5f5f5", color_palette="default"), layout=Layout(flex="1")),
    component_id="i114z",
    tag_name="main",
    display_order=1,
    custom_attributes={"id": "i114z"}
)
i114z_layout = Layout(flex="1")
i114z.layout = i114z_layout
i9wqu = ViewContainer(
    name="i9wqu",
    description=" component",
    view_elements={inhjk, i114z},
    styling=Styling(size=Size(height="100vh", font_family="Arial, sans-serif"), position=Position(display="flex"), color=Color(color_palette="default"), layout=Layout(layout_type=LayoutType.FLEX)),
    component_id="i9wqu",
    display_order=0,
    custom_attributes={"id": "i9wqu"}
)
i9wqu_layout = Layout(layout_type=LayoutType.FLEX)
i9wqu.layout = i9wqu_layout
wrapper_3.view_elements = {i9wqu}

gui_module = Module(
    name="GUI_Module",
    screens={wrapper, wrapper_2, wrapper_3}
)

# GUI Model
gui_model = GUIModel(
    name="GUI",
    package="",
    versionCode="1.0",
    versionName="1.0",
    modules={gui_module},
    description="GUI"
)
