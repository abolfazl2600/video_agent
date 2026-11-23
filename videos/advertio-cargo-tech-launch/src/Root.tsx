import React from 'react';
import {Composition} from 'remotion';
import {CargoLaunch} from './CargoLaunch';

export const Root: React.FC = () => (
  <>
    <Composition id="AdvertioCargoFinal" component={CargoLaunch}
      durationInFrames={600} fps={30} width={1920} height={1080}/>
    <Composition id="AdvertioCargoPreview" component={CargoLaunch}
      durationInFrames={300} fps={15} width={960} height={540}/>
  </>
);
