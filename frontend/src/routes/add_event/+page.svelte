<script lang="ts">
    import Icon from "$lib/components/Icon.svelte";
    import { getCookie } from "$lib/utils/utilCookie";
    import { BASE_URL } from "../../config";
    import { goto } from "$app/navigation";

    let title: string = '';
    let tags: string = '';
    let shortDescription: string = '';
    let longDescription: string = '';
    let date: string = '';
    let time: string = '';
    let location: string = '';
    let maxCountOfMembers: number;
    let format: 'offline' | 'online' | 'offline с трансляцией' = 'offline';
    let onlineEventLink: string = ' ';
    let file: FileList | null = null;

    let errors = {
        title: false,
        tags: false,
        shortDescription: false,
        longDescription: false,
        date: false,
        time: false,
        location: false,
        maxCountOfMembers: false,
        onlineEventLink: false,
    };

    const formatLabels = {
        offline: 'Офлайн',
        online: 'Онлайн',
        offline_with_streaming: 'Офлайн с трансляцией',
    };

    function validateFields(): boolean {
        errors = {
            title: !title.trim(),
            tags: !tags.trim(),
            shortDescription: !shortDescription.trim(),
            longDescription: !longDescription.trim(),
            date: !date.trim(),
            time: !time.trim(),
            location: !location.trim(),
            maxCountOfMembers: !maxCountOfMembers,
            onlineEventLink: (format === 'online' || format === 'offline с трансляцией') && !onlineEventLink.trim(),
        };

        return !Object.values(errors).some((error) => error);
    }

    async function createEvent(): Promise<void> {
        if (!validateFields()) {
            return;
        }

        const authToken: string | null = getCookie('auth_token');
        if (!authToken) {
            alert('Необходимо войти в систему!');
            return;
        }

        try {
            const dateObj = new Date(`${date}T${time}`);
            const formattedDate = `${dateObj.getFullYear()}-${String(dateObj.getMonth() + 1).padStart(2, '0')}-${String(dateObj.getDate()).padStart(2, '0')}`;
            const formattedTime = `${String(dateObj.getHours()).padStart(2, '0')}:${String(dateObj.getMinutes()).padStart(2, '0')}:${String(dateObj.getSeconds()).padStart(2, '0')}.${String(dateObj.getMilliseconds()).padStart(3, '0')}`;
            const eventDate = `${formattedDate} ${formattedTime}`;

            const formData: FormData = new FormData();
            formData.append('event_name', title);
            formData.append('place', location);
            formData.append('short_description', shortDescription);
            formData.append('long_description', longDescription);
            formData.append('max_count_of_members', maxCountOfMembers.toString());
            formData.append('format', format);
            formData.append('date', eventDate);
            formData.append('online_event_link', onlineEventLink || '');
            formData.append('tags', tags);

            if (file && file.length > 0) {
                formData.append('file', file[0]);
            }

            const response: Response = await fetch(`${BASE_URL}/events`, {
                method: 'POST',
                headers: {
                    'Authorization': `${authToken}`,
                },
                body: formData,
            });

            if (response.ok) {
                alert('Мероприятие создано!');
                goto('/lk/admin');
            } else {
                const errorText: string = await response.text();

                if (response.status === 403) {
                    alert('Эта функция доступна только для администраторов!');
                } else {
                    alert(`Ошибка при создании мероприятия: ${errorText}`);
                }
            }
        } catch (error: unknown) {
            if (error instanceof Error) {
                alert('Ошибка при отправке данных: ' + error.message);
            } else {
                alert('Произошла неизвестная ошибка');
            }
        }
    }
</script>

<Icon id="logo" />
<div class="page-background">
    <div class="content-container">
        <h1>Создание мероприятий</h1>
        <div class="container">
            <div class="form">
                <div class="form-column">
                    <input type="text" bind:value={title} placeholder="Название мероприятия" class:error={errors.title} />
                    <input type="text" bind:value={tags} placeholder="Теги (через пробел)" class:error={errors.tags} />
                    <textarea bind:value={shortDescription} placeholder="Короткое описание (до 150 символов)" class:error={errors.shortDescription}></textarea>
                    <textarea bind:value={longDescription} placeholder="Длинное описание" class:error={errors.longDescription}></textarea>
                    <div class="form-row">
                        <input type="time" bind:value={time} placeholder="Время" class:error={errors.time} />
                        <input type="date" bind:value={date} placeholder="Дата" class:error={errors.date} />
                        <input type="text" bind:value={location} placeholder="Место" class:error={errors.location} />
                    </div>
                    <div class="form-row narrow">
                        <input type="number" bind:value={maxCountOfMembers} placeholder="Макс. участников" class:error={errors.maxCountOfMembers} />
                        <select bind:value={format}>
                            <option value="offline">Офлайн</option>
                            <option value="online">Онлайн</option>
                            <option value="offline с трансляцией">Офлайн с трансляцией</option>
                        </select>
                    </div>
                    {#if format === 'online' || format === 'offline с трансляцией'}
                        <input type="text" bind:value={onlineEventLink} placeholder="Ссылка на онлайн мероприятие (если нет - пробел)" class:error={errors.onlineEventLink} />
                    {/if}
                    <input type="file" accept="image/*" bind:files={file} />
                </div>
            </div>
        </div>
        <div class="create-button-container">
            <button on:click={createEvent} class={format !== 'offline' ? 'full-width' : ''}>Создать</button>
        </div>
              
    </div>
</div>

<style>.error {
    border: 2px solid red;
}

.page-background {
    background-color: #171615;
    width: 100vw;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px;
    box-sizing: border-box;
    background-image: url('/createevent.png');
    background-size: cover;
    background-position: center center;
}

.content-container {
    width: 90%;
    max-width: 1300px;
    padding: 15px;
    margin-right: 40px;
}

h1 {
    font-size: 42px;
    font-family: "Font Over";
    color: white;
    margin-top: 80px;
    margin-bottom: 30px;
    text-align: left;
    width: 90%;
}

.container {
    width: 100%;
    padding: 15px;
    background-color: rgba(36, 36, 35, 0.5);
    border-radius: 40px;
    color: white;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.5);
    display: flex;
    flex-direction: column;
    gap: 40px;
    border: 1.3px solid rgba(255, 255, 255, 0.473);
}

.form {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
}

.form-column {
    display: flex;
    flex-direction: column;
    gap: 15px;
    flex: 1;
}

input,
textarea,
select {
    background-color: #171615;
    color: white;
    border: none;
    border-radius: 16px;
    padding: 20px;
    font-size: 16px;
}

textarea {
    min-height: 150px;
}


textarea:focus,
select:focus {
    outline: none;
    box-shadow: 0 0 5px rgba(255, 255, 255, 0.7);
}

.form-row {
    display: flex;
    gap: 15px;
    flex-wrap: wrap;
    width: 100%;
}

.form-row input,
.form-row select {
    flex: 1;
    min-width: 100px;
}

.form-row.narrow {
    justify-content: space-between;
}

.create-button-container {
    width: 100%;
    display: flex;
    justify-content: right; /* Выровнять кнопку по правому краю */
    margin-top: 20px;
}


.create-button-container button {
    padding: 10px 20px;
    font-size: 16px;
    color: white;
    background-color: #242423;
    border: 1.3px solid rgba(255, 255, 255, 0.473);
    border-radius: 30px;
    cursor: pointer;
    width: 200px;
    transition: background-color 0.3s;
}

.create-button-container button:hover {
    background-color: white;
    color: black;
}


.create-button-container button.full-width {
    width: 100%;
}

@media screen and (max-width: 1024px) {
    h1 {
        font-size: 28px;
        text-align: left;
    }

    .container {
        padding: 15px;
        border-radius: 25px;
        width: 108%;
    }

    .form {
        flex-direction: column;
        gap: 15px;
    }

    .form-row {
        flex-direction: column;
        gap: 15px;
    }

    input,
    textarea,
    select {
        font-size: 18px;
        padding: 15px;
    }

    .create-button-container {
        margin-top: 15px;
        text-align: center;
        margin-left: 15px;
    }

    .create-button-container button {
        width: 50%;
        font-size: 18px;
    }
}

@media screen and (max-width: 768px) {
    h1 {
        font-size: 24px;
        text-align: left;
        margin-bottom: 15px
    }

    .container {
        padding: 10px;
        border-radius: 20px;
        box-shadow: none;
        width: 105%;

    }

    .form {
        flex-direction: column;
        gap: 10px;
    }

    .form-row {
        flex-direction: column;
        gap: 10px;
    }

    input,
    textarea,
    select {
        font-size: 16px;
        padding: 10px;
    }

    .create-button-container {
        margin-top: 10px;
        text-align: center;
        margin-right: 10px;

    }

    .create-button-container button {
        width: 100%;
        font-size: 18px;
    }
}

@media screen and (max-width: 480px) {
    h1 {
        font-size: 22px;
    }

    .container {
        padding: 8px;
        border-radius: 15px;
    }

    .form {
        flex-direction: column;
        gap: 8px;
    }

    .form-row {
        flex-direction: column;
        gap: 8px;
    }

    input,
    textarea,
    select {
        font-size: 14px;
        padding: 8px;
    }

    .create-button-container {
        margin-top: 8px;
        text-align: center;
        margin-right: 10px;
    }

    .create-button-container button {
        width: 100%;
        font-size: 16px;
    }
}

</style>
