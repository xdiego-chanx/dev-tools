import { interruptible, requires } from "@main/lib";

export class ReactCommands {

    @interruptible()
    @requires("path")
    @requires("flat")
    public createPage(args: Map<ArgK, ArgV>): void {

    }
    
    @interruptible()
    @requires("path")
    @requires("flat")
    public createView(args: Map<ArgK, ArgV>): void {

    }
    
    @interruptible()
    @requires("path")
    @requires("flat")
    public createLayout(args: Map<ArgK, ArgV>): void {

    }
    
    @interruptible()
    @requires("path")
    @requires("flat")
    public createComponent(args: Map<ArgK, ArgV>): void {

    }
    
    @interruptible()
    @requires("path")
    @requires("flat")
    public createCssModule(args: Map<ArgK, ArgV>): void {

    }    
}