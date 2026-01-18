import React, { useRef, useState } from 'react';
import SignatureCanvasLib from 'react-signature-canvas';
import './SignatureCanvas.css';

interface SignatureCanvasProps {
  onSave: (signature: string) => void;
  disabled?: boolean;
  existingSignature?: string;
}

const SignatureCanvas: React.FC<SignatureCanvasProps> = ({ onSave, disabled, existingSignature }) => {
  const sigCanvas = useRef<SignatureCanvasLib>(null);
  const [isSigned, setIsSigned] = useState(!!existingSignature);

  const clearSignature = () => {
    sigCanvas.current?.clear();
    setIsSigned(false);
  };

  const saveSignature = () => {
    if (sigCanvas.current && !sigCanvas.current.isEmpty()) {
      const dataURL = sigCanvas.current.toDataURL('image/png');
      onSave(dataURL);
      setIsSigned(true);
    }
  };

  if (existingSignature) {
    return (
      <div className="signature-display">
        <img src={existingSignature} alt="Signature" className="signature-image" />
        <p className="signature-status">Signed</p>
      </div>
    );
  }

  return (
    <div className="signature-container">
      <div className="signature-canvas-wrapper">
        <SignatureCanvasLib
          ref={sigCanvas}
          penColor="black"
          canvasProps={{
            className: 'signature-canvas',
            width: 500,
            height: 200,
          }}
        />
      </div>

      <div className="signature-actions">
        <button
          type="button"
          onClick={clearSignature}
          className="btn btn-secondary"
          disabled={disabled}
        >
          Clear
        </button>
        <button
          type="button"
          onClick={saveSignature}
          className="btn btn-primary"
          disabled={disabled}
        >
          Save Signature
        </button>
      </div>

      {isSigned && <p className="signature-saved">Signature saved!</p>}
    </div>
  );
};

export default SignatureCanvas;
