import { interruptible, requires } from "@lib/decorators";

export class ConfigCommands {

    @interruptible()
    public explainConfigOptions(args: Map<ArgK, ArgV>): void {
        void args;
    }
    
    @interruptible()
    @requires("name")
    public getConfigProperty(args: Map<ArgK, ArgV>): void {

    }

    
    @interruptible()
    @requires("name")
    @requires("value")
    public putConfigProperty(args: Map<ArgK, ArgV>): void {

    }

    
    @interruptible()
    @requires("path")
    public getConfigProfile(args: Map<ArgK, ArgV>): void {

    }

    
    @interruptible()
    @requires("path")
    public putConfigProfile(args: Map<ArgK, ArgV>): void {

    }
}