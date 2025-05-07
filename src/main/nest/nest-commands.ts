import { interruptible, requires } from "@lib/decorators";

export class NestCommands {
    
    @interruptible()
    @requires("path")
    @requires("flat")
    public createResource(args: Map<ArgK, ArgV>): void {

    }

    
    @interruptible()
    @requires("path")
    @requires("flat")
    public createModule(args: Map<ArgK, ArgV>): void {

    }

    
    @interruptible()
    @requires("path")
    @requires("flat")
    public createController(args: Map<ArgK, ArgV>): void {

    }

    
    @interruptible()
    @requires("path")
    @requires("flat")
    public createService(args: Map<ArgK, ArgV>): void {

    }

    
    @interruptible()
    @requires("path")
    @requires("flat")
    @requires("orm")
    public createEntity(args: Map<ArgK, ArgV>): void {

    }

    
    @interruptible()
    @requires("path")
    @requires("flat")
    public createProject(args: Map<ArgK, ArgV>): void {

    }

    
    @interruptible()
    @requires("path")
    @requires("flat")
    public createMicroservice(args: Map<ArgK, ArgV>): void {

    }
}