import sys

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter
)

resource = Resource(attributes={"service.name": "plagiarism_system"})

tracer_provider = TracerProvider(resource=resource)

trace.set_tracer_provider(tracer_provider)

#console_exporter = ConsoleSpanExporter()

otlp_exporter = OTLPSpanExporter()

span_processor = BatchSpanProcessor(otlp_exporter)

tracer_provider.add_span_processor(span_processor)

tracer = trace.get_tracer(__name__)

from plagiarism_checker.plagiarism_system import Plagiarism_System

def main(): 
    with tracer.start_as_current_span(__name__) as span:
        if len(sys.argv) < 2: 
            sys.exit("please enter a filename for a document to check")
        input_file = sys.argv[1]
        system = Plagiarism_System(input_file, "docs/")
        system.compare()


if __name__ == "__main__": 
    main()