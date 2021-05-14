
export function norm(value:number, start:number, stop:number) : number {
    return start + (stop - start) * value;
}

export function lerp(start:number, stop:number, amt:number) : number {
    return (amt - start) / (stop - start);
}

export function interp_dict(v:number, a:Object, b:Object) : Object {
    let out = {};
    Object.keys(a).forEach(key => {
        out[key] = norm(v, a[key], b[key]);
    });
    return out;
}