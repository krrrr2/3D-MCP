// Node 에서 three.js 장면 코드를 돌리기 위한 최소 브라우저 대역 (형상만 필요, 텍스처는 버림)
function makeCtx(canvas) {
  const img = (w, h) => ({ width: w, height: h, data: new Uint8ClampedArray(Math.max(1, (w | 0) * (h | 0)) * 4) });
  const grad = () => ({ addColorStop() {} });
  return new Proxy({}, {
    get(_t, k) {
      if (k === 'canvas') return canvas;
      if (k === 'getImageData') return (x, y, w, h) => img(w, h);
      if (k === 'createImageData') return (w, h) => img(typeof w === 'object' ? w.width : w, typeof w === 'object' ? w.height : h);
      if (k === 'createLinearGradient' || k === 'createRadialGradient' || k === 'createConicGradient' || k === 'createPattern') return grad;
      if (k === 'measureText') return () => ({ width: 10 });
      if (k === 'getTransform') return () => ({ a: 1, b: 0, c: 0, d: 1, e: 0, f: 0 });
      return () => {};
    },
    set() { return true; },
  });
}
export function makeCanvas() {
  const c = { width: 1, height: 1, style: {}, toDataURL: () => 'data:,', addEventListener() {}, removeEventListener() {} };
  const ctx = makeCtx(c);
  c.getContext = () => ctx;
  return c;
}
globalThis.document = globalThis.document || { createElement: () => makeCanvas(), createElementNS: () => makeCanvas(), body: { appendChild() {} } };
globalThis.window = globalThis.window || globalThis;
globalThis.self = globalThis.self || globalThis;
globalThis.FileReader = class {
  readAsArrayBuffer(blob) { blob.arrayBuffer().then((b) => { this.result = b; this.onloadend?.(); this.onload?.({ target: this }); }); }
  readAsDataURL(blob) { blob.arrayBuffer().then((b) => { this.result = 'data:application/octet-stream;base64,' + Buffer.from(b).toString('base64'); this.onloadend?.(); this.onload?.({ target: this }); }); }
};
