import { Argument } from "./Argument";

export class Named<T extends ArgV> extends Argument {
    public flag: string;
    public abbr?: string;
    public def: T;

    constructor(name: string, help: string, def: T, abbr?: string) {
        super(name, help);
        this.flag = `--${name}`;
        this.def = def;
        this.abbr = abbr;
    }
}