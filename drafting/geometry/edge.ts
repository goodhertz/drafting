export enum Edge {
    MaxY,
    MaxX,
    MinY,
    MinX,
    MidY,
    MidX,
}

export type EdgePair = [Edge, Edge];

export function edgePairFromCompass(cmp:string) : EdgePair {
    let c = cmp.toUpperCase();
    switch (c) {
        case "C":
            return [Edge.MidX, Edge.MidY];
        case "W":
            return [Edge.MinX, Edge.MidY];
        case "NW":
            return [Edge.MinX, Edge.MaxY];
        case "N":
            return [Edge.MidX, Edge.MaxY];
        case "NE":
            return [Edge.MaxX, Edge.MaxY];
        case "E":
            return [Edge.MaxX, Edge.MidY];
        case "SE":
            return [Edge.MaxX, Edge.MinY];
        case "S":
            return [Edge.MidX, Edge.MinY];
        case "SW":
            return [Edge.MinX, Edge.MinY];
    }
}

export function txtToEdge(txt:string|Edge) : Edge {
    if (typeof(txt) !== "string") {
        return <Edge>txt;
    }

    let t = (<string>txt).toLowerCase();
    if (["maxy", "mxy", "n"].includes(t)) {
        return Edge.MaxY;
    } else if (["maxx", "mxx", "e"].includes(t)) {
        return Edge.MaxX;
    } else if (["miny", "mny", "s"].includes(t)) {
        return Edge.MinY;
    } else if (["minx", "mnx", "w"].includes(t)) {
        return Edge.MinX;
    } else if (["centery", "cy", "midy", "mdy"].includes(t)) {
        return Edge.MidY;
    } else if (["centerx", "cx", "midx", "mdx"].includes(t)) {
        return Edge.MidX;
    }
}