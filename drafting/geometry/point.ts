import { Geometrical } from "./geometrical";
import { norm } from "../interpolation";

export class Point extends Geometrical {
    x: number = 0;
    y: number = 0;

    constructor(points:Array<number|Point>) {
        super()
        let point = points[0];
        if (point instanceof Point) {
            this.x = point.x;
            this.y = point.y;
        } else {
            let pts = <Array<number>>points;
            this.x = pts[0];
            this.y = pts[1];
        }
    }

    offset(dx:number, dy:number) : Point {
        return new Point([this.x+dx, this.y+dy]);
    }

    round() : Point {
        return new Point([Math.round(this.x), Math.round(this.y)]);
    }

    roundTo(to:number) : Point {
        return new Point([Math.round(this.x/to)*to, Math.round(this.y/to)*to]);
    }

    xy() : Array<number> {
        return [this.x, this.y];
    }

    interp(v:number, other:Point, percent=false) : Point {
        let [sx, sy] = this.xy();
        let [ox, oy] = other.xy();
        v = percent ? v/100 : v;
        return new Point([(norm(v, sx, ox), norm(v, sy, oy))]);
    }
}