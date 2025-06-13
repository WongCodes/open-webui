<script lang="ts">
    import { onMount, getContext } from 'svelte';
    import { goto } from '$app/navigation';
    import { user } from '$lib/stores';
    import { getPlugins, getPluginConfig, setPluginConfig } from '$lib/apis/plugins';
    import Textarea from '$lib/components/common/Textarea.svelte';
    import { toast } from 'svelte-sonner';

    const i18n = getContext('i18n');

    let plugins: string[] = [];
    let selected = '';
    let configs: Record<string, any> = {};
    let configText = '';

    onMount(async () => {
        if ($user?.role !== 'admin') {
            await goto('/');
        }
        plugins = await getPlugins(localStorage.token).catch(() => []);
        if (plugins.length > 0) {
            selected = plugins[0];
            await loadConfig(selected);
        }
    });

    const loadConfig = async (name: string) => {
        const cfg = await getPluginConfig(localStorage.token, name).catch(() => ({}));
        configs[name] = cfg;
        configText = JSON.stringify(cfg, null, 2);
    };

    const save = async () => {
        try {
            const obj = JSON.parse(configText || '{}');
            configs[selected] = obj;
            await setPluginConfig(localStorage.token, selected, obj);
            toast.success(i18n.t('Settings saved successfully!'));
        } catch (e) {
            toast.error('Invalid JSON');
        }
    };
</script>

<div class="flex flex-col lg:flex-row w-full h-full pb-2 lg:space-x-4">
    <div class="flex flex-row overflow-x-auto gap-2.5 max-w-full lg:gap-1 lg:flex-col lg:flex-none lg:w-40 dark:text-gray-200 text-sm font-medium text-left scrollbar-none">
        {#each plugins as p}
            <button
                id={p}
                class="px-0.5 py-1 min-w-fit rounded-lg flex text-right transition {selected === p ? '' : 'text-gray-300 dark:text-gray-600 hover:text-gray-700 dark:hover:text-white'}"
                on:click={async () => { selected = p; await loadConfig(p); }}
            >
                <div class="self-center">{p}</div>
            </button>
        {/each}
    </div>
    <div class="flex-1 mt-1 lg:mt-0 space-y-2 overflow-y-scroll">
        {#if selected}
            <Textarea bind:value={configText} className="w-full h-40" />
            <button class="px-3 py-1 rounded bg-blue-600 text-white" on:click={save}>{i18n.t('Save')}</button>
        {/if}
    </div>
</div>
