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
    nest_feature_parser.add_argument("name", type=str, help="Name of the feature")
    nest_feature_parser.add_argument("--path", type=str, default=".", help="Target directory (default: .)")
    nest_feature_parser.add_argument("--js", action="store_true", help="Use JavaScript instead of TypeScript")
    nest_feature_parser.add_argument("--no-entity", action="store_true", help="Skip entity creation")
    nest_feature_parser.add_argument("--no-controller", action="store_true", help="Skip controller creation")
    nest_feature_parser.add_argument("--no-service", action="store_true", help="Skip service creation")
    nest_feature_parser.add_argument("--orm", type=str, default="typeorm", help="ORM to use (default: typeorm)")
    nest_feature_parser.add_argument("--use-uuid", action="store_true", default=True, help="Use UUIDs (default: true)")

    # devtools nest module
    nest_module_parser = nest_subparsers.add_parser("module", help="Create a NestJS module")
    nest_module_parser.add_argument("name", type=str, help="Name of the module")
    nest_module_parser.add_argument("--path", type=str, default=".", help="Target directory (default: .)")
    nest_module_parser.add_argument("--js", action="store_true", help="Use JavaScript instead of TypeScript")
    
    # devtools nest controller
    nest_controller_parser = nest_subparsers.add_parser("controller", help="Create a NestJS controller")
    nest_controller_parser.add_argument("name", type=str, help="Name of the controller")
    nest_controller_parser.add_argument("--path", type=str, default=".", help="Target directory (default: .)")
    nest_controller_parser.add_argument("--js", action="store_true", help="Use JavaScript instead of TypeScript")
    
    # devtools nest service
    nest_service_parser = nest_subparsers.add_parser("service", help="Create a NestJS service")
    nest_service_parser.add_argument("name", type=str, help="Name of the service")
    nest_service_parser.add_argument("--path", type=str, default=".", help="Target directory (default: .)")
    nest_service_parser.add_argument("--js", action="store_true", help="Use JavaScript instead of TypeScript")
    
    # devtools nest entity
    nest_entity_parser = nest_subparsers.add_parser("entity", help="Create a NestJS entity")
    nest_entity_parser.add_argument("name", type=str, help="Name of the entity")
    nest_entity_parser.add_argument("--path", type=str, default=".", help="Target directory (default: .)")
    nest_entity_parser.add_argument("--js", action="store_true", help="Use JavaScript instead of TypeScript")
    nest_entity_parser.add_argument("--orm", type=str, default="typeorm", help="ORM to use (default: typeorm)")
    nest_entity_parser.add_argument("--use-uuid", action="store_true", default=True, help="Use UUIDs (default: true)")

    # devtools nest microservice
    nest_microservice_parser = nest_subparsers.add_parser("microservice", help="Create a NestJS microservice project")
    nest_microservice_parser.add_argument("name", type=str, help="Name of the microservice")
    nest_microservice_parser.add_argument("--path", type=str, default=".", help="Target directory (default: .)")
    nest_microservice_parser.add_argument("--js", action="store_true", help="Use JavaScript instead of TypeScript")

    # devtools react
    react_parser = subparsers.add_parser("react", help="React-related utilities")
    react_subparsers = react_parser.add_subparsers(dest="react_command")
    
    # devtools react view
    react_view_parser = react_subparsers.add_parser("view", help="Create a React view")
    
    react_view_parser.add_argument("name", type=str, help="Name of the view or component")
    react_view_parser.add_argument("--path", type=str, default=".", help="Target directory (default '.')")
    react_view_parser.add_argument("--css", action="store_true", help="Include a CSS module file")
    react_view_parser.add_argument("--tsx", action="store_true", help="Use TypeScript JSX (.tsx)")
    react_view_parser.add_argument("--layout", action="store_true", help="Include a layout file")
    
    # devtools react component
    react_component_parser = react_subparsers.add_parser("component", help="Create a React component")
    
    react_component_parser.add_argument("name", type=str, help="Name of the view or component")
    react_component_parser.add_argument("--path", type=str, default=".", help="Target directory (default '.')")
    react_component_parser.add_argument("--css", action="store_true", help="Include a CSS module file")
    react_component_parser.add_argument("--new-dir", action="store_true", help="Create files inside a new directory")
    react_component_parser.add_argument("--tsx", action="store_true", help="Use TypeScript JSX (.tsx)")
    
    args = parser.parse_args()

    if args.command == "react": # devtools react
        if args.react_command == "view": # devtools react view
            react.view(args.name, args.path, args.css, args.layout, args.tsx)
        elif args.react_command == "component": #devtools react component
            react.component(args.name, args.path, args.css, args.tsx)
    if args.command == "nest": # devtools nest
        if args.nest_command == "feature": # devtools nest feature
            nest.feature(args.name, args.path, args.orm, args.use_uuid, args.js, args.no_entity, args.no_controller, args.no_service)
        elif args.nest_command == "module": # devtools nest module
            nest.module(args.name, args.path, args.js)
        elif args.nest_command == "controller": # devtools nest controller
            nest.controller(args.name, args.path, args.js)
        elif args.nest_command == "service": # devtools nest service
            nest.service(args.name, args.path, args.js)
        elif args.nest_command == "entity": # devtools nest entity
            nest.entity(args.name, args.path, args.js, args.orm, args.use_uuid)
        elif args.nest_command == "microservice": # devtools nest microservice
            nest.microservice(args.name, args.path, args.js)
        
    
if __name__ == "__main__":
    main()
