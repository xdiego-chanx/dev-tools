import { Case } from "./case";

export class CasingManager {
    private static readonly _instance = new CasingManager();

    private constructor() { }

    public static get instance() {
        return CasingManager._instance;
    }

    private toSpaced(name: string, casing: Case): string[] {
        switch (casing) {
            case Case.Camel:
            case Case.Pascal:
                return this.splitAtUpper(name);
            case Case.Snake:
            case Case.Upper:
                return name.toLowerCase().split("_");
            case Case.Kebab:
                return name.toLowerCase().split("-");
            case Case.Spaced:
                return name.toLowerCase().split(" ");
            case Case.Uri:
                return decodeURIComponent(name).toLowerCase().split(" ");
        }
    }

    private toCasing(name: string[], casing: Case): string {
        switch (casing) {
            case Case.Camel:
                return name[0].toLowerCase() + name.slice(1).map((w) => w.capitalize()).join("");
            case Case.Pascal:
                return name.map((w) => w.capitalize()).join("");
            case Case.Snake:
                return name.join("_").toLowerCase();
            case Case.Upper:
                return name.join("_").toUpperCase();
            case Case.Kebab:
                return name.join("-").toLowerCase();
            case Case.Spaced:
                return name.join(" ").toLowerCase();
            case Case.Uri:
                return encodeURIComponent(name.join(" ").toLowerCase());
        }
    }

    private splitAtUpper(name: string): string[] {
        let words: Array<string> = []
        let start = 0
        name = name.removePrefix(/^_+/).removeSuffix(/_+$/);

        for (let i = 0; i < name.length; i++) {
            let current = name[i]
            let last = name[i - 1]
            let next = null;
            if (i + 1 < name.length) {
                next = name[i + 1]
            }

            if (!Number.isDigit(current) && !Number.isDigit(last)) {
                words.push(name.slice(start, i));
                start = i;
            } else if (current.isUpperCase()) {
                if (last == last.toLowerCase()) {
                    words.push(name.slice(start, i));
                    start = i;
                } else if (next && next.isLowerCase()) {
                    words.push(name.slice(start, i));
                    start = i;
                } else if (next && next.isUpperCase()) {
                    continue;
                }
            }
        }
        words.push(name.slice(start));
        return words.map((word) => word.toLowerCase());
    }

    public change(name: string, from: Case, to: Case) {
        return this.toCasing(this.toSpaced(name, from), to);
    }
}
