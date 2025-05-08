class TraverseError extends Error {
    constructor(message: string) {
        super(message);
    }
}

class Parse {
    public logger: any;
    public name: string;
    public help: string;

    public positionals: Array<{ [key: string]: any }>;
    public named: Array<{ [key: string]: any }>;

    public argumentMap: Map<string, any>;
    public subcommands: Map<string, any >;

    public parse(args: Array<string>) {

        const namedArguments = args.slice(this.positionals.length);

        this.named.forEach((named) => {
            const argument = namedArguments.find((arg) => arg == named.abbr || arg == named.flag);
            if (!argument) {
                this.argumentMap.set(named.name, named.def);
                return;
            }
            const index = namedArguments.indexOf(argument);

            let key: string | undefined = undefined;
            let value: string | undefined = undefined;

            switch (typeof named.def) {
                case "number":
                    if (argument.includes("=")) {
                        [key, value] = argument.split("=");
                    } else {
                        [key, value] = [argument, namedArguments[index + 1]];
                    }

                    if (!value) {
                        throw new TypeError("Required argument '" + named.name + "' is missing a value.")
                    }

                    if (Number.isNaN(parseFloat(value))) {
                        throw new TypeError("Argument '" + key + "' expects a number. got 'string' instead.");
                    }
                    this.argumentMap.set(named.name, parseFloat(value));
                    break;

                case "string":
                    if (argument.includes("=")) {
                        [key, value] = argument.split("=");
                    } else {
                        [key, value] = [argument, namedArguments[index + 1]];
                    }

                    if (!value) {
                        throw new TypeError("Required argument '" + named.name + "' is missing a value.")
                    }

                    this.argumentMap.set(named.name, value);
                    break;

                case "boolean":
                    if (argument.includes("=")) {
                        [key, value] = argument.split("=");
                    }

                    if (value) {
                        if (["true", "on"].includes(value)) {
                            this.argumentMap.set(named.name, true);
                        } else if (["false", "off"].includes(value)) {
                            this.argumentMap.set(named.name, false);
                        } else {
                            throw new TypeError("Argument '" + key + "' expects a switch (true/false || on/off). got 'string' instead.");
                        }
                    } else {
                        if (key) {
                            this.argumentMap.set(named.name, true);
                        } else {
                            this.argumentMap.set(named.name, named.def);
                        }
                    }
                    break;

                default:
                    throw new TypeError("Argument of type '" + typeof named.def + "' is not assignable to parameter of type 'number | string | boolean'.");
            }
        });
    }
    observer(argumentMap: any) {
        throw new Error("Method not implemented.");
    }
    buildHelpString(): any {
        throw new Error("Method not implemented.");
    }
}