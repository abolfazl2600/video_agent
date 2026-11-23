import React from 'react';
import {Composition} from 'remotion';
import {CargoReels} from './CargoReels';

// Native portrait framing, not a crop of the old 16:9 composition.
export const Root: React.FC = () => (
  <>
    <Composition id="AdvertioCargoFinal" component={CargoReels}
      durationInFrames={600} fps={30} width={1080} height={1920}/>
    <Composition id="AdvertioCargoPreview" component={CargoReels}
      durationInFrames={300} fps={15} width={540} height={960}/>
  </>
);
