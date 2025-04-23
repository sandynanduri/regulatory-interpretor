CDM Main Components:
The CDM has seven main modeling dimensions:
Product model
Event model
Legal agreements
Process model
Reference data model
Mapping
Namespace
Event-Related Files:
The event-related files are primarily in the rosetta-source/src/main/rosetta directory:
event-common-type.rosetta - Core event types
event-common-func.rosetta - Event functions
event-common-enum.rosetta - Event enumerations
event-workflow-type.rosetta - Workflow types
event-workflow-func.rosetta - Workflow functions
event-workflow-enum.rosetta - Workflow enumerations
event-position-type.rosetta - Position types
event-position-func.rosetta - Position functions
event-position-enum.rosetta - Position enumerations
event-qualification-func.rosetta - Qualification functions
Event Mappings:
The event mappings can be found in several mapping files:
mapping-fpml-confirmation-workflowstep-synonym.rosetta - FpML confirmation workflow mappings
mapping-fpml-confirmation-tradestate-synonym.rosetta - FpML confirmation trade state mappings
mapping-cme-synonym.rosetta - CME mappings
mapping-dtcc-synonym.rosetta - DTCC mappings
mapping-fis-synonym.rosetta - FIS mappings
Key Event Components:
Business Events: Represent events that occur during the lifecycle of a trade
Workflow Steps: Represent the state of a business event
Event Timestamps: Track when events occur
Event Identifiers: Provide unique IDs for events
Event Instructions: Specify how to create business events
Event Types:
The CDM supports various event types including:
Execution events
Amendment events
Termination events
Reset events
Payment events
Novation events
And more
The event model is designed to be flexible and comprehensive, allowing for precise tracking of all aspects of trade lifecycle events. The mappings ensure compatibility with existing industry messaging formats like FpML, CME, and DTCC.


Rules generation, improved agent terminal, MCP images.
