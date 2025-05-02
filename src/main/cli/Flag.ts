import { Argument } from "./Argument";

export class Flag extends Argument {
    public flag: string;
    public abbr?: string;

    constructor(name: string, abbr?: string) {
        super(name);

        this.flag = `--${name}`;
        this.abbr = abbr;
    }
}