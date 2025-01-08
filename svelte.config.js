// import adapter from '@sveltejs/adapter-auto';
// import preprocess from 'svelte-preprocess';
import adapter from "@sveltejs/adapter-static"; 

const dev = "production" === "development";

/** @type {import('@sveltejs/kit').Config} */
const config = {

	// // note that previous projects have included this preprocess, but I don't think it's necessary, we'll see when build
	// preprocess: preprocess(),

	kit: {
		// adapter-auto only supports some environments, see https://kit.svelte.dev/docs/adapter-auto for a list.
		// If your environment is not supported, or you settled on a specific environment, switch out the adapter.
		// See https://kit.svelte.dev/docs/adapters for more information about adapters.
		adapter: adapter({
		    pages: "docs",
		    assets: "docs"
		}),
		paths: {
		    // change below to your repo name
		    base: dev ? "" : "/rail-transit-and-population-density",
		}
	}
};

export default config;