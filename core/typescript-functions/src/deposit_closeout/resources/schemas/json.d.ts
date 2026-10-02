/** Static bundled schema imports; no filesystem or SDK access in domain code. */
declare module "*.schema.json" {
  const schema: unknown;
  export default schema;
}
