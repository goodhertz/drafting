import { Geometrical } from './geometrical';
import { Point } from './point';
import { Edge, txtToEdge, edgePairFromCompass } from './edge';

const COMMON_PAPER_SIZES = {
    'letter': [612, 792],
    'tabloid': [792, 1224],
    'ledger': [1224, 792],
    'legal': [612, 1008],
    'a0': [2384, 3371],
    'a1': [1685, 2384],
    'a2': [1190, 1684],
    'a3': [842, 1190],
    'a4': [595, 842],
    'a4Small': [595, 842],
    'a5': [420, 595],
    'b4': [729, 1032],
    'b5': [516, 729],
    'folio': [612, 936],
    'quarto': [610, 780],
    '10x14': [720, 1008],
};

export interface Rectlike extends Geometrical {
    x: number;
    y: number;
    w: number;
    h: number;
}

export function align(b:Rectlike, rect:Rect, xEdge:Edge|string=Edge.MidX, yEdge:Edge|string=Edge.MidY) : Point {
    let x = txtToEdge(xEdge);
    let y = txtToEdge(yEdge);
    
    let xoff = 0;
    if (x == Edge.MidX) {
        xoff = -b.x + rect.x + rect.w/2 - b.w/2;
    } else if (x == Edge.MinX) {
        xoff = -(b.x-rect.x);
    } else if (x == Edge.MaxX) {
        xoff = -b.x + rect.x + rect.w - b.w;
    }
    
    let yoff = 0;
    if (y == Edge.MidY) {
        yoff = -b.y + rect.y + rect.h/2 - b.h/2
    } else if (y == Edge.MaxY) {
        yoff = (rect.y + rect.h) - (b.h + b.y)
    } else if (y == Edge.MinY) {
        yoff = -(b.y-rect.y)
    }
    
    return new Point([xoff, yoff]);
}

export class Rect implements Rectlike {
    x: number;
    y: number;
    w: number;
    h: number;

    constructor() {
        super();
    }
}