// Claude Code mark — original SVG path lifted from plugin/dashboard/public/
// claudecode-color.svg and inlined here so it ships with the JS bundle (no
// extra request, can size with a prop). Eye cutouts use fill-rule evenodd.
export function ClaudeIcon({ size = 14 }: { size?: number }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      xmlns="http://www.w3.org/2000/svg"
      style={{
        display: "inline-block",
        verticalAlign: "-0.18em",
        flexShrink: 0,
        marginRight: 4,
      }}
      role="img"
      aria-label="Claude Code"
    >
      <title>Claude Code</title>
      <path
        fill="#D97757"
        fillRule="evenodd"
        clipRule="evenodd"
        d="M20.998 10.949H24v3.102h-3v3.028h-1.487V20H18v-2.921h-1.487V20H15v-2.921H9V20H7.488v-2.921H6V20H4.487v-2.921H3V14.05H0V10.95h3V5h17.998v5.949zM6 10.949h1.488V8.102H6v2.847zm10.51 0H18V8.102h-1.49v2.847z"
      />
    </svg>
  );
}
