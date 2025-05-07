import { interruptible, requires } from "@main/lib";

export class TypescriptCommands {
    
    @interruptible()
    @requires("path")
    @requires("flat")
    public createClass(args: Map<ArgK, ArgV>): void {

    }

    @interruptible()
    @requires("path")
    @requires("flat")
    public createInterface(args: Map<ArgK, ArgV>): void {

    }

    @interruptible()
    @requires("path")
    @requires("flat")
    public createEnum(args: Map<ArgK, ArgV>): void {

    }

    @interruptible()
    @requires("path")
    @requires("flat")
    public createBarrel(args: Map<ArgK, ArgV>): void {

    }
}