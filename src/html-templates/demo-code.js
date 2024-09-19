
                const videoId = "6f214f93-f682-4024-b2dd-9f81f69a03a6";
                const url = "https://movio-cdn.algocode.site/segments/aaab9653-c84f-45f4-b94a-c6c4e7669670__test2/manifest.mpd";

                const player = dashjs.MediaPlayer().create();
                player.initialize(document.querySelector("#videoPlayer"), url, true);

                player.on("error", function (e) {
                        console.error("DASH player error:", e);
                });

                player.on("initialized", function () {
                        console.log("DASH player initialized.");
                });

                player.on("streaming:bufferingCompleted", function () {
                        console.log("Buffering completed.");
                });

                player.on("streamInitialized", function () {
                        const availableTracks = player.getTracksFor('text');
                        console.log("Available subtitle tracks:", availableTracks);

                        availableTracks.forEach(track => {
                                player.setTextTrack(track.index);
                                console.log(`Enabled subtitle track: ${track.lang}`);
                        });

                        createSubtitleUI(availableTracks);
                });

                function createSubtitleUI(tracks) {
                        const container = document.createElement('div');
                        container.id = 'subtitleSelector';

                        const select = document.createElement('select');
                        select.addEventListener('change', (e) => {
                                player.setTextTrack(parseInt(e.target.value));
                        });

                        const noneOption = document.createElement('option');
                        noneOption.value = -1;
                        noneOption.textContent = 'No subtitles';
                        select.appendChild(noneOption);

                        tracks.forEach((track, index) => {
                                const option = document.createElement('option');
                                option.value = index;
                                option.textContent = `Subtitles: ${track.lang}`;
                                select.appendChild(option);
                        });

                        container.appendChild(select);
                        document.body.appendChild(container);
                }