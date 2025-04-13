import argparse

from .react import commands as react
from .nest import commands as nest

def main():
    parser = argparse.ArgumentParser(prog="devtools", description="A CLI for development tools.")
    subparsers = parser.add_subparsers(dest="command")

    # devtools nest
    nest_parser = subparsers.add_parser("nest", help="Nest-related utilities")
    nest_subparsers = nest_parser.add_subparsers(dest="nest_command")

    # devtools nest feature
    nest_feature_parser = nest_subparsers.add_parser("feature", help="Create a NestJS feature")
    nest_feature_parser.add_argument("path", type=str, help="Target directory")
    nest_feature_parser.add_argument("--js", action="store_true", help="Use JavaScript instead of TypeScript")
    nest_feature_parser.add_argument("--no-entity", action="store_true", help="Skip entity creation")
    nest_feature_parser.add_argument("--no-controller", action="store_true", help="Skip controller creation")
    nest_feature_parser.add_argument("--no-service", action="store_true", help="Skip service creation")
    nest_feature_parser.add_argument("--orm", type=str, default="typeorm", help="ORM to use (default: typeorm)")
    nest_feature_parser.add_argument("--no-uuid", action="store_true", help="Use auto-incrementing integers instead of UUIDs (default: false)")
    nest_feature_parser.add_argument("--flat", action="store_true", help="Create files in the current directory instead of creating a new one (default: false)")

    # devtools nest module
    nest_module_parser = nest_subparsers.add_parser("module", help="Create a NestJS module")
    nest_module_parser.add_argument("path", type=str, help="Target directory")
    nest_module_parser.add_argument("--js", action="store_true", help="Use JavaScript instead of TypeScript")
    nest_module_parser.add_argument("--flat", action="store_true", help="Create files in the current directory instead of creating a new one (default: false)")

    # devtools nest controller
    nest_controller_parser = nest_subparsers.add_parser("controller", help="Create a NestJS controller")
    nest_controller_parser.add_argument("path", type=str, help="Target directory")
    nest_controller_parser.add_argument("--js", action="store_true", help="Use JavaScript instead of TypeScript")
    nest_controller_parser.add_argument("--flat", action="store_true", help="Create files in the current directory instead of creating a new one (default: false)")

    # devtools nest service
    nest_service_parser = nest_subparsers.add_parser("service", help="Create a NestJS service")
    nest_service_parser.add_argument("path", type=str, help="Target directory")
    nest_service_parser.add_argument("--js", action="store_true", help="Use JavaScript instead of TypeScript")
    nest_service_parser.add_argument("--flat", action="store_true", help="Create files in the current directory instead of creating a new one (default: false)")

    # devtools nest entity
    nest_entity_parser = nest_subparsers.add_parser("entity", help="Create a NestJS entity")
    nest_entity_parser.add_argument("path", type=str, help="Target directory")
    nest_entity_parser.add_argument("--js", action="store_true", help="Use JavaScript instead of TypeScript")
    nest_entity_parser.add_argument("--orm", type=str, default="typeorm", help="ORM to use (default: typeorm)")
    nest_entity_parser.add_argument("--no-uuid", action="store_true", default=True, help="Use auto-incrementing integers instead of UUIDs (default: false)")
    nest_entity_parser.add_argument("--flat", action="store_true", help="Create files in the current directory instead of creating a new one (default: false)")

    # devtools nest microservice
    nest_microservice_parser = nest_subparsers.add_parser("microservice", help="Create a NestJS microservice project")
    nest_microservice_parser.add_argument("path", type=str, help="Target directory")
    nest_microservice_parser.add_argument("--js", action="store_true", help="Use JavaScript instead of TypeScript")
    
    # devtools react
    react_parser = subparsers.add_parser("react", help="React-related utilities")
    react_subparsers = react_parser.add_subparsers(dest="react_command")
    
    # devtools react view
    react_view_parser = react_subparsers.add_parser("view", help="Create a React view")
    
    react_view_parser.add_argument("path", type=str, help="Target directory")
    react_view_parser.add_argument("--css", action="store_true", help="Include a CSS module file")
    react_view_parser.add_argument("--tsx", action="store_true", help="Use TypeScript JSX (.tsx)")
    react_view_parser.add_argument("--layout", action="store_true", help="Include a layout file")
    react_view_parser.add_argument("--flat", action="store_true", help="Create files in the current directory instead of creating a new one (default: false)")

    
    # devtools react component
    react_component_parser = react_subparsers.add_parser("component", help="Create a React component")
    
    react_component_parser.add_argument("path", type=str, help="Target directory")
    react_component_parser.add_argument("--css", action="store_true", help="Include a CSS module file")
    react_component_parser.add_argument("--tsx", action="store_true", help="Use TypeScript JSX (.tsx)")
    react_component_parser.add_argument("--flat", action="store_true", help="Create files in the current directory instead of creating a new one (default: false)")
    
    args = parser.parse_args()

    if args.command == "react": # devtools react
        if args.react_command == "view": # devtools react view
            react.view(args.path, args.css, args.layout, args.tsx, args.flat)
        elif args.react_command == "component": #devtools react component
            react.component(args.path, args.css, args.tsx, args.flat)
    if args.command == "nest": # devtools nest
        if args.nest_command == "feature": # devtools nest feature
            nest.feature(args.path, args.orm, not args.no_uuid, args.js, args.no_entity, args.no_controller, args.no_service, args.flat)
        elif args.nest_command == "module": # devtools nest module
            nest.module(args.path, args.js, args.flat)
        elif args.nest_command == "controller": # devtools nest controller
            nest.controller(args.path, args.js, args.flat)
        elif args.nest_command == "service": # devtools nest service
            nest.service(args.path, args.js, args.flat)
        elif args.nest_command == "entity": # devtools nest entity
            nest.entity(args.path, args.js, args.orm, not args.no_uuid, args.flat)
        elif args.nest_command == "microservice": # devtools nest microservice
            nest.microservice(args.path, args.js)
        
    
if __name__ == "__main__":
    main()
